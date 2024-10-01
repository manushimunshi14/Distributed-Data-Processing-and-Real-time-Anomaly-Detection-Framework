from kafka import KafkaConsumer
import json
from kafka.admin import KafkaAdminClient
from kafka.errors import NoBrokersAvailable
import csv
import time
from pyspark.ml import PipelineModel
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, year, month, dayofweek, hour, date_format
from pyspark.ml.feature import OneHotEncoder, StringIndexer, VectorAssembler
from pyspark.ml import Pipeline
from pyspark.sql.functions import lit
from pyspark.ml.classification import GBTClassifier

spark = SparkSession.builder.appName("ML").getOrCreate()

train_data = spark.read.csv("train-data.csv", header=True, inferSchema=True)

windowSize = 10000

def train_model(training_data):
    categorical_cols = ["EventType", "Location", "Severity", "Day_of_Week", "Year_Month"]
    indexers = [StringIndexer(inputCol=col, outputCol=col+"_index", handleInvalid="keep") for col in categorical_cols]
    encoder = [OneHotEncoder(inputCol=indexer.getOutputCol(), outputCol=col+"_encoded") for indexer, col in zip(indexers, categorical_cols)]
    feature_cols = ["EventType_encoded", "Location_encoded", "Severity_encoded", "Day_of_Week_encoded", "Year_Month_encoded", "Hour_of_Day"]
    assembler = VectorAssembler(inputCols=feature_cols, outputCol="features")

    gbt = GBTClassifier(featuresCol='features', labelCol='Is_Anomaly', predictionCol='prediction')
    pipeline_stages_gbt = indexers + encoder + [assembler, gbt]
    pipeline_gbt = Pipeline(stages=pipeline_stages_gbt)

    pipeline_model = pipeline_gbt.fit(training_data)

    return pipeline_model

def preprocess_data(message):
    df = spark.createDataFrame([message])

    df = df.drop("Details")

    df = df.withColumn("Year_Month", date_format(col("Timestamp"), "yyyy-MM")) \
           .withColumn("Day_of_Week", date_format(col("Timestamp"), "E")) \
           .withColumn("Hour_of_Day", hour(col("Timestamp")))

    df = df.drop("Timestamp")

    return df

print("Loading model....")

loaded_model_gbt = PipelineModel.load("./gbt_model")

print("Model loaded.")

def establish_connection(bootstrap_servers):
    try:
        admin_client = KafkaAdminClient(
            bootstrap_servers=bootstrap_servers, request_timeout_ms=500
        )
        admin_client.close()
        return True
    except NoBrokersAvailable:
        return False

print("Initializing consumer...")
consumer = KafkaConsumer(
    'health_events',
    bootstrap_servers=['44.201.154.178:9092'],
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

while True:
    if establish_connection('kafka:9092'):
        print("Connection established with broker")
        break
    else:
        print(
            "Retrying to connect to broker in 5 seconds..."
        )
        time.sleep(5)

message_count = 0

for message in consumer:
    print("-----------------------------------------")
    print("Message consumed.")
    
    df = preprocess_data(message)
    
    df_with_anomaly = df.withColumn("Is_Anomaly", lit(0))

    train_data = train_data.union(df_with_anomaly.select(train_data.columns))
    
    predictions = loaded_model_gbt.transform(train_data)

    prediction_result = predictions.select("prediction").collect()

    train_data = train_data.withColumn("Is_Anomaly", predictions["prediction"].cast("integer"))

    # Check if the window size is reached
    if message_count == windowSize:
        # Retrain the model
        retrained_model = train_model(train_data)

        # Save the retrained model, replacing the previous one
        retrained_model.write().overwrite().save("./gbt_model")

        # Refreshing the model after retraining
        loaded_model_gbt = PipelineModel.load("./gbt_model")

        message_count = 0

    message_count += 1

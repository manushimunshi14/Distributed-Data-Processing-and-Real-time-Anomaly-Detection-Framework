from kafka import KafkaConsumer
import json
from kafka.admin import KafkaAdminClient
from kafka.errors import NoBrokersAvailable
import time
from pyspark.ml import PipelineModel
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, year, month, dayofweek, hour, date_format

spark = SparkSession.builder.appName("ML").getOrCreate()

windowSize = 5

def preprocess_data(message):
    # Create DataFrame from message
    df = spark.createDataFrame([message])

    # Drop the Details column if it exists
    df = df.drop("Details")

    # Split the Timestamp column into different components
    df = df.withColumn("Year_Month", date_format(col("Timestamp"), "yyyy-MM")) \
           .withColumn("Day_of_Week", date_format(col("Timestamp"), "E")) \
           .withColumn("Hour_of_Day", hour(col("Timestamp")))

    # Drop the Timestamp column
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

# Accumulator to store messages for each window
message_accumulator = []

# Counter for messages received
message_count = 0

for message in consumer:
    print("-----------------------------------------")
    print("Message consumed.")
    
    # Preprocess the message and add it to the accumulator
    df = preprocess_data(message)
    message_accumulator.append(df)
    
    message_count += 1
    
    # Check if the window size is reached
    if message_count == windowSize:
        # Concatenate all DataFrames in the accumulator
        df_window = spark.union(message_accumulator)
        
        # Make predictions using the loaded GBT model
        predictions = loaded_model_gbt.transform(df_window)

        # Extract prediction results
        prediction_result = predictions.select("prediction").collect()
        print("Predictions:", prediction_result)
        
        # Clear the accumulator and reset message count
        message_accumulator = []
        message_count = 0
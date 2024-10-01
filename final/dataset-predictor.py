import sys
from pyspark.ml import PipelineModel
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, year, month, dayofweek, hour, date_format
import os

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <input_file_path> <output_file_path>")
        sys.exit(1)

    input_file_path = sys.argv[1]
    output_file_path = sys.argv[2]

    spark = SparkSession.builder.appName("ML").getOrCreate()

    loaded_model_gbt = PipelineModel.load("./gbt_model")

    health_data_df = spark.read.csv(input_file_path, header=True, inferSchema=True)

    health_data_df = health_data_df.drop("Details")

    health_data_df = health_data_df.withColumn("Year_Month", date_format(col("Timestamp"), "yyyy-MM")) \
        .withColumn("Day_of_Week", date_format(col("Timestamp"), "E")) \
        .withColumn("Hour_of_Day", hour(col("Timestamp")))

    health_data_df = health_data_df.drop("Timestamp")

    predictions_df = loaded_model_gbt.transform(health_data_df)

    if os.path.exists(output_file_path):
        os.remove(output_file_path)

    predictions_with_renamed_column_df = predictions_df.select("EventType", "Location", "Severity", "prediction").withColumnRenamed("prediction", "Is_Anomaly")

    predictions_with_renamed_column_df.write.csv(output_file_path, header=True, mode="overwrite")

    spark.stop()
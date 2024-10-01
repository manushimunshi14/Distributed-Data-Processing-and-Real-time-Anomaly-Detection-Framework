import pytest
from unittest.mock import patch, MagicMock
from kafka import KafkaConsumer
import json
from kafka.admin import KafkaAdminClient
from kafka.errors import NoBrokersAvailable
import csv
import time
from pyspark.ml import PipelineModel
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, year, month, dayofweek, hour, date_format, lit
from pyspark.ml.feature import OneHotEncoder, StringIndexer, VectorAssembler
from pyspark.ml import Pipeline
from pyspark.ml.classification import GBTClassifier
from retrainModel import train_model

def test_train_model():

    spark = SparkSession.builder.appName("ML").getOrCreate()
    train_data = spark.read.csv("train-data.csv", header=True, inferSchema=True)
    expected_model = PipelineModel.load("../gbt_model")
    result_model = train_model(train_data)
    assert result_model.stages == expected_model.stages

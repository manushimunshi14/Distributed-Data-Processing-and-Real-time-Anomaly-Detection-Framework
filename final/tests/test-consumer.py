import pytest
from unittest.mock import patch, MagicMock
from kafka import KafkaConsumer
import json
from kafka.admin import KafkaAdminClient
from kafka.errors import NoBrokersAvailable
import csv
import time
import psycopg2
from consumer import establish_connection

@patch('kafka.admin.KafkaAdminClient')
def test_establish_connection(mock_KafkaAdminClient):
    mock_admin_client = MagicMock()
    mock_KafkaAdminClient.return_value = mock_admin_client
    bootstrap_servers = 'kafka:9092'
    result = establish_connection(bootstrap_servers)
    assert result == True
    mock_KafkaAdminClient.assert_called_once_with(bootstrap_servers=bootstrap_servers, request_timeout_ms=500)
    mock_admin_client.close.assert_called_once()

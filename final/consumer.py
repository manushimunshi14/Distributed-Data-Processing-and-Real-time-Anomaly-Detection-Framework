from kafka import KafkaConsumer
import json
import csv
from kafka.admin import KafkaAdminClient
from kafka.errors import NoBrokersAvailable
import time
import psycopg2


csv_file = open('health_data.csv', 'a', newline='')
csv_writer = csv.writer(csv_file)

target_host = "postgres"
target_database = "health_data_db"
target_username = "root"
target_password = "password"
target_port = "5432"

# Parameters to the new database where we push the transformed data to connect to it
dest_conn = psycopg2.connect(
    host=target_host,
    database=target_database,
    user=target_username,
    password=target_password,
    port=target_port
)
dest_cur = dest_conn.cursor()

print("Connected to database.")

# Create a new table in the new database
create_table_sql = """
CREATE TABLE IF NOT EXISTS health_data (
    EventType VARCHAR,
    Timestamp TIMESTAMP WITH TIME ZONE,
    Location VARCHAR,
    Severity VARCHAR,
    Details TEXT
);
"""
dest_cur.execute(create_table_sql)
dest_conn.commit()

print("Table created.")
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

for message in consumer:
    print ("-----------------------------------------")
    print("Message consumed.")

    csv_writer.writerow([
        message.value['EventType'],
        message.value['Timestamp'],
        message.value['Location'],
        message.value['Severity'],
        message.value['Details'],
    ])

    print("Message inserted into CSV file.")

    insert_query = """
    INSERT INTO health_data (EventType, Timestamp, Location, Severity, Details)
    VALUES (%s, %s, %s, %s, %s);
    """

    # Execute the insert query with the message data
    dest_cur.execute(insert_query, (message.value['EventType'], message.value['Timestamp'], message.value['Location'], message.value['Severity'], message.value['Details']))
    dest_conn.commit()

    print("Message inserted into PostgreSQL database.")

csv_file.close()
dest_cur.close()
dest_conn.close()

from kafka import KafkaConsumer, KafkaProducer
import json
import csv
from kafka.admin import KafkaAdminClient, NewTopic
from kafka.errors import TopicAlreadyExistsError, NoBrokersAvailable
import time

csv_file = open('health_data.csv', 'a', newline='')
csv_writer = csv.writer(csv_file)

def create_topics(admin_client):
    try:
        topics = [
            NewTopic(name='hospital_admissions', num_partitions=1, replication_factor=1),
            NewTopic(name='emergency_incident', num_partitions=1, replication_factor=1),
            NewTopic(name='vaccination', num_partitions=1, replication_factor=1),
            NewTopic(name='high', num_partitions=1, replication_factor=1),
            NewTopic(name='medium', num_partitions=1, replication_factor=1),
            NewTopic(name='low', num_partitions=1, replication_factor=1)
        ]
        admin_client.create_topics(new_topics=topics, validate_only=False)
        print("Topics created successfully")
    except TopicAlreadyExistsError:
        print("Topics already exist")
    except Exception as e:
        print("Error creating topics:", e)

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

producer = KafkaProducer( bootstrap_servers='kafka:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8'))

admin_client = KafkaAdminClient(bootstrap_servers='kafka:9092')

create_topics(admin_client)
admin_client.close()

for message in consumer:
    print ("-----------------------------------------")
    print("Message consumed.")
    # for key, value in message.value.items():
    #     print(f"{key}: {value}")
    event_type = message.value['EventType']
    if event_type in ['hospital_admission', 'emergency_incident', 'vaccination']:
        producer.send(event_type, value=message.value)
        print("Sent to event topic:", event_type)
    else:
        print("Not Relevant Event Type:", event_type)

    severity = message.value['Severity']
    if severity in ['high', 'medium', 'low']:
        producer.send(severity, value=message.value)
        print("Sent to severity topic:", severity)
    else:
        print("Not Relevant Severity:", severity)

    producer.flush()

    csv_writer.writerow([
        message.value['EventType'],
        message.value['Timestamp'],
        message.value['Location'],
        message.value['Severity'],
        message.value['Details'],
    ])

csv_file.close()
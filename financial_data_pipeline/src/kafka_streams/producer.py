import csv
import time
from kafka import KafkaProducer
import json
import os
import pandas as pd
import numpy as np

# Kafka producer settings
KAFKA_TOPIC = os.environ.get("KAFKA_TOPIC", '')
KAFKA_BROKER = 'localhost:9092'
CSV_FILE_PATH = 'data/trans.csv'


# Create Kafka producer
producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER,
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)


def read_csv_and_send_to_kafka(file_path):
    # Check if the file exists
	if not os.path.isfile(file_path):
		raise FileNotFoundError(f"CSV file not found: {file_path}")

	# Open the CSV file
	records = pd.read_csv(file_path, nrows=500).replace({np.nan:None}).to_dict(orient='records')

	for row in records:
		producer.send(KAFKA_TOPIC, value=row)
		print(f"Sent: {row}")
		time.sleep(1)  # Simulate real-time data streaming


if __name__ == "__main__":
    if KAFKA_TOPIC == '':
        print("Topic Value is empty")
        exit(0)

    try:
        # Call the function to read CSV and send data to Kafka
        read_csv_and_send_to_kafka(CSV_FILE_PATH)
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        producer.flush()
        producer.close()

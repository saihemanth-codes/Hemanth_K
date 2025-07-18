from pyspark.sql import SparkSession
import os, time
from datetime import datetime, timezone

kafka_topic = os.environ.get("KAFKA_TOPIC", '')
checkpoint_location = f"/checkpoint/dev/financial_data_pipeline/{kafka_topic}/"

spark = SparkSession.builder \
    .appName("KafkaToHadoopStreaming") \
    .config("spark.sql.streaming.checkpointLocation", checkpoint_location) \
    .getOrCreate()

# schema for the incoming data
schema = """
    trans_id LONG,
    account_id STRING,
    date DATE,
    type STRING,
    operation STRING,
    amount DOUBLE,
    balance DOUBLE,
    k_symbol STRING,
    bank STRING,
    account LONG
"""

# Read from Kafka
df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", kafka_topic) \
    .load()

# Define the schema of the data (if known) and cast the value to string
parsed_df = df.selectExpr("CAST(value AS STRING)") \
    .selectExpr("CAST(value AS STRING) as json") \
    .selectExpr("from_json(json, '{}') as data".format(schema)) \
    .select("data.*")

# Write the stream to HDFS in csv format
query = parsed_df.writeStream \
    .outputMode("append") \
    .format("parquet") \
    .option("path", "/user/root/data/transactions") \
    .option("checkpointLocation", checkpoint_location) \
    .start()

idle_timeout = 10  # Terminate if idle for 60 seconds

# Function to check if the query is idle
def is_idle(query):
    # Check the latest batch processing time
    current_time = datetime.now(timezone.utc).replace(tzinfo=None)
    if query.lastProgress is None:
        return False
    last_batch_time = datetime.strptime(query.lastProgress.get('timestamp', current_time).split('.')[0], "%Y-%m-%dT%H:%M:%S") #2024-09-14T16:44:11.503Z

    # Determine if the idle timeout has been exceeded
    if (current_time - last_batch_time).seconds >= idle_timeout:
        return True
    return False


# Monitor the streaming query
try:
    while True:
        # Wait for the query to make progress
        time.sleep(1)  # Check every 10 seconds

        # Check if the query is idle
        if is_idle(query):
            print(f"Streaming query has been idle for {idle_timeout} seconds. Stopping...")
            query.stop()
            break

except KeyboardInterrupt:
    print("Streaming job interrupted by user.")
finally:
    # Ensure the query is stopped gracefully
    if query.isActive:
        query.stop()
    spark.stop()

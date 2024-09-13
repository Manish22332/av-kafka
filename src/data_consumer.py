import json
import boto3
from kafka import KafkaConsumer
from config import s3_config  # Your S3 configuration file

# Initialize S3 client
s3_client = boto3.client(
    's3',
    aws_access_key_id=s3_config['aws_access_key_id'],
    aws_secret_access_key=s3_config['aws_secret_access_key'],
    region_name=s3_config['region_name']
)

S3_BUCKET = s3_config['bucket_name']
KAFKA_TOPIC = 'oakd-lidar-stream'
KAFKA_SERVER = 'localhost:9092'

# Initialize Kafka Consumer
consumer = KafkaConsumer(KAFKA_TOPIC,
                         bootstrap_servers=KAFKA_SERVER,
                         value_deserializer=lambda m: json.loads(m.decode('utf-8')))

def save_to_s3(data):
    # Create a unique file name based on timestamp
    file_name = f"oakd_lidar_data_{data['timestamp']}.json"
    
    # Save the data as a JSON file in the S3 bucket
    s3_client.put_object(Body=json.dumps(data), Bucket=S3_BUCKET, Key=file_name)
    print(f"Saved data to S3: {file_name}")

def consume_data():
    for message in consumer:
        data = message.value
        save_to_s3(data)

if __name__ == '__main__':
    print("Starting Kafka consumer...")
    consume_data()

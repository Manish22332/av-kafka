import json
import boto3
from kafka import KafkaProducer, KafkaConsumer

def get_s3_client():
    """Create an S3 client using configuration."""
    with open("config/s3_config.json") as f:
        s3_config = json.load(f)

    return boto3.client(
        "s3",
        aws_access_key_id=s3_config["aws_access_key_id"],
        aws_secret_access_key=s3_config["aws_secret_access_key"],
        region_name=s3_config["region_name"],
    )

def upload_to_s3(bucket_name, file_name, data):
    """Upload data to an S3 bucket."""
    s3_client = get_s3_client()
    s3_client.put_object(Bucket=bucket_name, Key=file_name, Body=json.dumps(data))

def get_kafka_producer():
    """Create a Kafka producer."""
    return KafkaProducer(
        bootstrap_servers="localhost:9092",
        value_serializer=lambda v: json.dumps(v).encode("utf-8"),
    )

def get_kafka_consumer(topic):
    """Create a Kafka consumer."""
    return KafkaConsumer(
        topic,
        bootstrap_servers="localhost:9092",
        auto_offset_reset="earliest",
        enable_auto_commit=True,
        value_deserializer=lambda x: json.loads(x.decode("utf-8")),
    )

# Oak-D and Intel Lidar Kafka Stream to S3

This project demonstrates how to set up a Kafka stream to collect data from the OAK-D camera and Intel Lidar, then process and store the data in an Amazon S3 bucket. The data is streamed to a Kafka topic, consumed by a Kafka consumer, and uploaded to S3 for storage.

## Step 1: Folder Structure

```
oakd-lidar-kafka-stream/
│
├── config/
│   ├── kafka.properties             # Kafka producer/consumer configurations
│   ├── s3_config.json               # AWS S3 bucket configuration
│
├── src/
│   ├── main.py                     # Main script to initialize Kafka producers and consumers
│   ├── data_producer.py            # Kafka producer to stream OAK-D and Intel Lidar data
│   ├── data_consumer.py            # Kafka consumer that writes data to S3
│   ├── utils.py                    # Helper functions for Kafka connection, S3 uploads
│
├── requirements.txt                # Python dependencies
├── README.md                       # Project documentation
├── Dockerfile                      # Dockerfile for containerized deployment
├── docker-compose.yml               # Docker Compose file for setting up Kafka
```

## Step 2: Prerequisites

1. **Docker**: Ensure you have Docker installed for running Kafka using Docker Compose.
2. **AWS S3**: An Amazon S3 account to store the streamed data.
3. **OAK-D Camera and Intel Lidar**: Data collection devices for streaming.

## Step 3: Install Dependencies

Create a virtual environment and install the necessary dependencies listed in `requirements.txt`:

```bash
python3 -m venv venv
source venv/bin/activate 
pip install -r requirements.txt
```

## Step 4: Run Kafka Using Docker Compose

Run Kafka using Docker Compose:

```bash
docker-compose up -d
```

This will start a Kafka and Zookeeper instance in the background.

## Step 5: Configure AWS S3

Create a configuration file `config/s3_config.json` with your AWS credentials and S3 bucket information:

```json
{
    "aws_access_key_id": "your-access-key",
    "aws_secret_access_key": "your-secret-key",
    "region_name": "us-east-1",
    "bucket_name": "your-bucket-name"
}
```

## Step 6: Run the Application

1. **Start the Kafka Producer**:
   ```bash
   python src/data_producer.py
   ```

2. **Start the Kafka Consumer**:
   ```bash
   python src/data_consumer.py
   ```

3. **Run Everything Together**:
   ```bash
   python src/main.py
   ```

## Step 7: Docker Deployment (Optional)

To run the application in a containerized environment, use the provided `Dockerfile`.

### Build the Docker Image

```bash
docker build -t oakd-lidar-app .
```

### Run the Producer and Consumer in Containers

1. **Run the Producer Container**:
   ```bash
   docker run -d --network=host --name producer oakd-lidar-app python src/data_producer.py
   ```

2. **Run the Consumer Container**:
   ```bash
   docker run -d --network=host --name consumer oakd-lidar-app python src/data_consumer.py
   ```

### Notes:
- `--network=host` ensures the containers can communicate with Kafka on `localhost:9092`.
- Each container runs its respective script.

## Step 8: Troubleshooting

- **Kafka Connection Issues**: Ensure Kafka is running on the correct host and port (`localhost:9092` by default).
- **S3 Uploads Not Working**: Double-check your AWS credentials and S3 bucket permissions.
- **Data Capture from OAK-D and Intel Lidar**: Replace the dummy data with actual data capture logic from the devices. You may need additional SDKs or libraries to interface with them.




import json
import time
import depthai as dai  # OAK-D SDK
import pyrealsense2 as rs  # Intel RealSense SDK
from kafka import KafkaProducer

# Kafka configuration
KAFKA_BROKER = "localhost:9092"
TOPIC_NAME = "oakd-lidar-stream"

# Initialize Kafka producer
producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER,
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

# Initialize Intel RealSense pipeline
def initialize_lidar():
    pipeline = rs.pipeline()
    config = rs.config()
    config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
    pipeline.start(config)
    return pipeline

# Get LiDAR data
def get_lidar_data(pipeline):
    frames = pipeline.wait_for_frames()
    depth_frame = frames.get_depth_frame()
    
    if not depth_frame:
        return None

    width, height = depth_frame.get_width(), depth_frame.get_height()
    center_distance = depth_frame.get_distance(width // 2, height // 2)  # Get center point depth

    return {
        "distance": round(center_distance, 2),
        "angle": 0  # Adjust if actual angle data is needed
    }

# Initialize OAK-D Camera
def initialize_oakd():
    pipeline = dai.Pipeline()
    
    cam = pipeline.create(dai.node.ColorCamera)
    cam.setPreviewSize(640, 480)
    cam.setInterleaved(False)
    cam.setColorOrder(dai.ColorCameraProperties.ColorOrder.RGB)
    
    xout = pipeline.create(dai.node.XLinkOut)
    xout.setStreamName("video")
    cam.preview.link(xout.input)
    
    device = dai.Device(pipeline)
    return device, device.getOutputQueue(name="video", maxSize=4, blocking=False)

# Get OAK-D Data
def get_oakd_data(queue):
    frame = queue.get()
    image_data = frame.getCvFrame()  # Get the frame as OpenCV format

    return {
        "depth": 0,  # OAK-D provides depth through a separate depth stream
        "color": image_data.tolist()  # Convert image to a list (can be optimized)
    }

# Main producer loop
def produce_sensor_data():
    lidar_pipeline = initialize_lidar()
    oakd_device, oakd_queue = initialize_oakd()

    while True:
        lidar_data = get_lidar_data(lidar_pipeline)
        oakd_data = get_oakd_data(oakd_queue)

        if lidar_data and oakd_data:
            data = {
                "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
                "lidar_data": lidar_data,
                "oakd_data": oakd_data
            }

            producer.send(TOPIC_NAME, value=data)
            print(f"Produced: {json.dumps(data, indent=2)}")  # Debugging output
        
        time.sleep(1)

if __name__ == "__main__":
    print("Starting Kafka producer with real sensor data...")
    produce_sensor_data()

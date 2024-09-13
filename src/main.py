from data_producer import stream_data
from data_consumer import consume_data
import threading

def main():
    # Start data producer in a separate thread
    producer_thread = threading.Thread(target=stream_data)
    producer_thread.start()
    
    # Start data consumer in the main thread
    consume_data()

if __name__ == '__main__':
    main()

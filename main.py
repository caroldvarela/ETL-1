from src.streaming.kafka_utils import kafka_producer, kafka_consumer
import threading

if __name__ == "__main__":
    producer_thread = threading.Thread(target=kafka_producer)
    consumer_thread = threading.Thread(target=kafka_consumer)

    producer_thread.start()
    consumer_thread.start()

    producer_thread.join()
    consumer_thread.join()
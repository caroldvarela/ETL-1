from kafka import KafkaProducer, KafkaConsumer
from json import dumps, loads
import time
import pandas as pd


def kafka_producer(data):
    producer = KafkaProducer(
        value_serializer=lambda m: dumps(m).encode('utf-8'),
        bootstrap_servers=['localhost:9092'],
    )
    
    for index in range(len(data)):
        time.sleep(3)  
        row = data.iloc[index].to_dict()
        producer.send("kafka_project", value=row)  
        print(f"Message sent: {row}\n")

    producer.flush() 

def kafka_consumer():
    consumer = KafkaConsumer(
        'kafka_project',
        #auto_offset_reset='lastest',
        enable_auto_commit=True,
        group_id='my-group-1',
        value_deserializer=lambda m: loads(m.decode('utf-8')),
        bootstrap_servers=['localhost:9092']
    )

    try:
        for m in consumer:
            print(f"Message received: {m.value}\n")
    except Exception as e:
        print(f"Error: {e}")
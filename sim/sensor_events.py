from kafka import KafkaProducer
import json, time, random

producer = KafkaProducer(bootstrap_servers="localhost:9092", value_serializer=lambda v: json.dumps(v).encode())

shelves = ["A", "B"]

while True:
    event = {
        "shelf_id": random.choice(shelves),
        "ts": time.time(),
        "delta_g": random.choice([-50, 50])  # pick or put
    }
    producer.send("sensor", event)
    print("Sensor Event:", event)
    time.sleep(3)

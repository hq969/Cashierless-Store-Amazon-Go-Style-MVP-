from kafka import KafkaProducer
import json, time, random

producer = KafkaProducer(bootstrap_servers="localhost:9092", value_serializer=lambda v: json.dumps(v).encode())

shelves = ["A", "B"]

while True:
    event = {
        "person_id": f"user_{random.randint(1000,9999)}",
        "shelf_id": random.choice(shelves),
        "sku_guess": random.choice(["COKE", "CHIPS"]),
        "ts": time.time(),
        "event_type": "hand_in_roi"
    }
    producer.send("vision", event)
    print("Vision Event:", event)
    time.sleep(2)

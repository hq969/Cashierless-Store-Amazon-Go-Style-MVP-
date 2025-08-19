import time
import json
import numpy as np
from scipy.optimize import linear_sum_assignment
from kafka import KafkaConsumer, KafkaProducer
from services.db import engine
from sqlalchemy import text
from datetime import datetime

producer = KafkaProducer(bootstrap_servers="localhost:9092", value_serializer=lambda v: json.dumps(v).encode())
vision_consumer = KafkaConsumer("vision", bootstrap_servers="localhost:9092", value_deserializer=lambda m: json.loads(m.decode()))
sensor_consumer = KafkaConsumer("sensor", bootstrap_servers="localhost:9092", value_deserializer=lambda m: json.loads(m.decode()))

def fuse_event(hand, spike):
    action = "add" if spike["delta_g"] < 0 else "remove"
    return {
        "person_id": hand["person_id"],
        "shelf_id": hand["shelf_id"],
        "sku": hand["sku_guess"],
        "action": action,
        "ts": spike["ts"]
    }

def save_to_cart(ev):
    with engine.begin() as conn:
        if ev["action"] == "add":
            conn.execute(text("INSERT INTO cart_line (person_id, sku, qty, unit_price, ts) VALUES (:p,:s,:q,:u,:t)"),
                         {"p": ev["person_id"], "s": ev["sku"], "q": 1, "u": 40, "t": datetime.utcnow()})
        elif ev["action"] == "remove":
            conn.execute(text("DELETE FROM cart_line WHERE person_id=:p AND sku=:s LIMIT 1"),
                         {"p": ev["person_id"], "s": ev["sku"]})

def run_fusion():
    hands, spikes = [], []
    while True:
        for msg in vision_consumer:
            hands.append(msg.value)
        for msg in sensor_consumer:
            spikes.append(msg.value)
        for h in hands:
            for s in spikes:
                if h["shelf_id"] == s["shelf_id"] and abs(h["ts"] - s["ts"]) < 1.0:
                    ev = fuse_event(h, s)
                    save_to_cart(ev)
                    producer.send("fusion", ev)

if __name__ == "__main__":
    run_fusion()

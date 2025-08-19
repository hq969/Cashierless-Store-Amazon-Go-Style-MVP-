import requests, time

print("=== Shopper enters ===")
resp = requests.post("http://localhost:8000/enter", json={})
pid = resp.json()["person_id"]
print("Person ID:", pid)

print("=== Waiting for shopper to pick items (fusion running) ===")
time.sleep(10)

print("=== Shopper exits ===")
resp = requests.post(f"http://localhost:8000/exit/{pid}")
print("Receipt:", resp.json())

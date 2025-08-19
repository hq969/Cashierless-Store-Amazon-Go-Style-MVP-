import yaml
from collections import defaultdict

# Load shelf config
with open("edge/config.yaml") as f:
    config = yaml.safe_load(f)
shelves = {s["id"]: s for s in config["shelves"]}

# Virtual carts
carts = defaultdict(list)

def fuse_event(person_id, shelf_id, delta_g):
    shelf = shelves[shelf_id]
    action = "add" if delta_g < 0 else "remove"

    if action == "add":
        carts[person_id].append(shelf["sku"])
        print(f"[+] {person_id} picked {shelf['sku']}")
    else:
        if shelf["sku"] in carts[person_id]:
            carts[person_id].remove(shelf["sku"])
            print(f"[-] {person_id} returned {shelf['sku']}")

    return carts[person_id]

def get_cart(person_id):
    return carts[person_id]

# data.py
# Simulated database using a list of dictionaries (mock storage)

inventory = [
    {
        "id": 1,
        "product_name": "Chocolate Milk",
        "brands": "Fairlife",
        "ingredients_text": "Ultra-filtered milk, sugar, cocoa processed with alkali, ...",
        "price": 5.99,
        "stock": 25
    }
]
next_id = 2  # keeps track of the next available ID


def get_all_items():
    return inventory

# --- GET ---
def get_item(item_id):
    for item in inventory:
        if item["id"] == item_id:
            return item
    return None

# --- ADD ---
def add_item(data):
    global next_id
    data["id"] = next_id
    inventory.append(data)
    next_id += 1
    return data

# --- UPDATE ---
def update_item(item_id, data):
    item = get_item(item_id)
    if item:
        item.update(data)
        return item
    return None

# --- DELETE ---
def delete_item(item_id):
    item = get_item(item_id)
    if item:
        inventory.remove(item)
        return True
    return False
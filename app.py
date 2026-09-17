# app.py
from flask import Flask, jsonify, request
import data
import external_api

app = Flask(__name__)


# GET /inventory -> returns all items in the inventory
@app.route("/inventory", methods=["GET"])
def get_inventory():
    return jsonify(data.get_all_items())


# GET /inventory/<id> -> returns a single item by ID
@app.route("/inventory/<int:item_id>", methods=["GET"])
def get_single_item(item_id):
    item = data.get_item(item_id)
    if item:
        return jsonify(item)
    return jsonify({"error": "Item not found"}), 404  # 404 = not found


# POST /inventory -> adds a new item using JSON sent in the request body
@app.route("/inventory", methods=["POST"])
def create_item():
    new_data = request.get_json()  # parse incoming JSON body
    created = data.add_item(new_data)
    return jsonify(created), 201  # 201 = created


# PATCH /inventory/<id> -> updates an existing item with JSON sent in the request body
@app.route("/inventory/<int:item_id>", methods=["PATCH"])
def update_existing_item(item_id):
    updates = request.get_json()
    updated = data.update_item(item_id, updates)
    if updated:
        return jsonify(updated)
    return jsonify({"error": "Item not found"}), 404


# DELETE /inventory/<id> -> removes an item by ID
@app.route("/inventory/<int:item_id>", methods=["DELETE"])
def remove_item(item_id):
    success = data.delete_item(item_id)
    if success:
        return jsonify({"message": "Item deleted"})
    return jsonify({"error": "Item not found"}), 404


# GET /lookup/<barcode> -> looks up a product on OpenFoodFacts by barcode
@app.route("/lookup/<barcode>", methods=["GET"])
def lookup_by_barcode(barcode):
    product = external_api.fetch_by_barcode(barcode)
    if product:
        return jsonify(product)
    return jsonify({"error": "Product not found"}), 404


# GET /lookup/name/<name> -> looks up a product on OpenFoodFacts by name
@app.route("/lookup/name/<name>", methods=["GET"])
def lookup_by_name(name):
    product = external_api.fetch_by_name(name)
    if product:
        return jsonify(product)
    return jsonify({"error": "Product not found"}), 404



# Runs the app in debug mode when this file is executed directly
if __name__ == "__main__":
    app.run(debug=True)
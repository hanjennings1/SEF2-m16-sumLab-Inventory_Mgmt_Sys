# tests/test_app.py
import pytest
import app as flask_app
import data


@pytest.fixture
def client():
    """Provides a Flask test client, and resets the mock inventory before each test."""
    flask_app.app.config["TESTING"] = True

    # reset inventory data before each test so tests don't affect each other
    data.inventory.clear()
    data.inventory.append({
        "id": 1,
        "product_name": "Test Product",
        "brands": "Test Brand",
        "ingredients_text": "Test ingredients",
        "price": 1.99,
        "stock": 10
    })
    data.next_id = 2

    with flask_app.app.test_client() as client:
        yield client


# === GET TESTS ===
def test_get_all_items(client):
    response = client.get("/inventory")
    assert response.status_code == 200
    assert len(response.get_json()) == 1

def test_get_single_item_found(client):
    response = client.get("/inventory/1")
    assert response.status_code == 200
    assert response.get_json()["product_name"] == "Test Product"

def test_get_single_item_not_found(client):
    response = client.get("/inventory/999")
    assert response.status_code == 404


# === CREATE ITEM TEST ===
def test_create_item(client):
    new_item = {
        "product_name": "New Product",
        "brands": "New Brand",
        "ingredients_text": "Some ingredients",
        "price": 5.49,
        "stock": 20
    }
    response = client.post("/inventory", json=new_item)
    assert response.status_code == 201

    data_returned = response.get_json()
    assert data_returned["product_name"] == "New Product"
    assert data_returned["id"] == 2  # should be auto-assigned since id 1 already exists


# === UPDATE ITEM TESTS ===
def test_update_item_found(client):
    response = client.patch("/inventory/1", json={"price": 9.99})
    assert response.status_code == 200
    assert response.get_json()["price"] == 9.99

def test_update_item_not_found(client):
    response = client.patch("/inventory/999", json={"price": 9.99})
    assert response.status_code == 404


# === DELETE ITEM TESTS ===
def test_delete_item_found(client):
    response = client.delete("/inventory/1")
    assert response.status_code == 200
    # confirm it's actually gone:
    check = client.get("/inventory/1")
    assert check.status_code == 404

def test_delete_item_not_found(client):
    response = client.delete("/inventory/999")
    assert response.status_code == 404
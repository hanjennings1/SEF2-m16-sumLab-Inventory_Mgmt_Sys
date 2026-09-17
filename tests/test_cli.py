# tests/test_cli.py
from unittest.mock import patch, MagicMock
import cli


# === ADD ITEM TESTS ===
@patch("cli.requests.post")
@patch("builtins.input")
def test_add_item_success(mock_input, mock_post, capsys):
    # simulate user typing these values in order, one per input() call
    mock_input.side_effect = ["Mock Product", "Mock Brand", "Mock Ingredients", "4.99", "10"]

    mock_response = MagicMock()
    mock_response.status_code = 201
    mock_response.json.return_value = {"id": 1, "product_name": "Mock Product"}
    mock_post.return_value = mock_response

    cli.add_item()

    captured = capsys.readouterr()  # grabs everything printed during the function call
    assert "Item added" in captured.out

@patch("builtins.input")
def test_add_item_invalid_price(mock_input, capsys):
    # simulate user typing a non-numeric price
    mock_input.side_effect = ["Mock Product", "Mock Brand", "Mock Ingredients", "not_a_number", "10"]

    cli.add_item()

    captured = capsys.readouterr()
    assert "Invalid" in captured.out



# === VIEW INVENTORY TEST ===
@patch("cli.requests.get")
@patch("builtins.input")
def test_view_all_items(mock_input, mock_get, capsys):
    mock_input.side_effect = ["1"]  # choose "View all items"

    mock_response = MagicMock()
    mock_response.json.return_value = [{"id": 1, "product_name": "Mock Product"}]
    mock_get.return_value = mock_response

    cli.view_inventory()

    captured = capsys.readouterr()
    assert "Mock Product" in captured.out



# === UPDATE ITEM TEST ===
@patch("cli.requests.patch")
@patch("builtins.input")
def test_update_item_success(mock_input, mock_patch, capsys):
    # simulate: item ID, field choice "1" (price), new value
    mock_input.side_effect = ["1", "1", "9.99"]

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"id": 1, "price": 9.99}
    mock_patch.return_value = mock_response

    cli.update_item()

    captured = capsys.readouterr()
    assert "Item updated" in captured.out



# === DELETE ITEM TEST ===
@patch("cli.requests.delete")
@patch("builtins.input")
def test_delete_item_success(mock_input, mock_delete, capsys):
    mock_input.side_effect = ["1"]  # item ID to delete

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_delete.return_value = mock_response

    cli.delete_item()

    captured = capsys.readouterr()
    assert "Item deleted" in captured.out
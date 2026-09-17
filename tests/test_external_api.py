# tests/test_external_api.py
from unittest.mock import patch, MagicMock
import external_api



# === FETCH BY BARCODE TESTS ===
@patch("external_api.requests.get")
def test_fetch_by_barcode_found(mock_get):
    # simulate a successful OpenFoodFacts response
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "status": 1,
        "product": {"product_name": "Mock Product", "brands": "Mock Brand"}
    }
    mock_get.return_value = mock_response

    result = external_api.fetch_by_barcode("1234567890123")

    assert result["product_name"] == "Mock Product"
    mock_get.assert_called_once()  # confirm requests.get was actually called

@patch("external_api.requests.get")
def test_fetch_by_barcode_not_found(mock_get):
    # simulate OpenFoodFacts saying the barcode doesn't exist:
    mock_response = MagicMock()
    mock_response.json.return_value = {"status": 0}
    mock_get.return_value = mock_response

    result = external_api.fetch_by_barcode("0000000000000")

    assert result is None



# === FETCH BY NAME TESTS ===
@patch("external_api.requests.get")
def test_fetch_by_name_found(mock_get):
    # simulate a search-a-licious response with one matching hit:
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "hits": [{"product_name": "Mock Search Result", "brands": ["Mock Brand"]}]
    }
    mock_get.return_value = mock_response

    result = external_api.fetch_by_name("mock product")

    assert result["product_name"] == "Mock Search Result"

@patch("external_api.requests.get")
def test_fetch_by_name_not_found(mock_get):
    # simulate no matching products found:
    mock_response = MagicMock()
    mock_response.json.return_value = {"hits": []}
    mock_get.return_value = mock_response

    result = external_api.fetch_by_name("nonexistent product")

    assert result is None
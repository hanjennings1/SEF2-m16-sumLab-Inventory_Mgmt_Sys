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
    # simulate a search-a-licious response with one matching hit (full raw shape)
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "hits": [{
            "product_name": "Mock Search Result",
            "brands": ["Mock Brand"],
            "ingredients_text": "mock ingredients",
            "code": "1234567890123",
            "extra_field_we_dont_care_about": "should be ignored"
        }]
    }
    mock_get.return_value = mock_response

    result = external_api.fetch_by_name("mock product")

    # confirm only the expected fields are extracted
    assert result == {
        "product_name": "Mock Search Result",
        "brands": ["Mock Brand"],
        "ingredients_text": "mock ingredients",
        "code": "1234567890123"
    }

@patch("external_api.requests.get")
def test_fetch_by_name_not_found(mock_get):
    mock_response = MagicMock()
    mock_response.json.return_value = {"hits": []}
    mock_get.return_value = mock_response

    result = external_api.fetch_by_name("nonexistent product")

    assert result is None

@patch("external_api.requests.get")
def test_fetch_by_name_missing_fields(mock_get):
    # simulate a product missing some fields (like ingredients_text = null we saw in Postman)
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "hits": [{"product_name": "Partial Product", "code": "999"}]
    }
    mock_get.return_value = mock_response

    result = external_api.fetch_by_name("partial")

    assert result["product_name"] == "Partial Product"
    assert result["brands"] is None  # missing field should safely become None
    assert result["ingredients_text"] is None
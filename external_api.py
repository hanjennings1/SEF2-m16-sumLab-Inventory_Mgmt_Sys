# external_api.py
import requests

BASE_URL = "https://world.openfoodfacts.org"

# OpenFoodFacts requires a descriptive User-Agent header to avoid 403 errors
HEADERS = {
    "User-Agent": "InventoryManagementApp/1.0 (school-lab-project)"
}

def fetch_by_barcode(barcode):
    """Fetch a single product by exact barcode."""
    url = f"{BASE_URL}/api/v2/product/{barcode}.json"
    response = requests.get(url, headers=HEADERS)    # send GET request to OpenFoodFacts
    result = response.json()        # convert response body into a Python dict

    if result.get("status") == 1:   # status 1 = product was found
        return result["product"]
    return None                     # barcode not found


def fetch_by_name(name):
    """Search for products by name using Open Food Facts' full-text search engine."""
    url = "https://search.openfoodfacts.org/search"
    params = {"q": name, "page_size": 1}
    response = requests.get(url, params=params, headers=HEADERS)
    result = response.json()

    products = result.get("hits", [])  # search-a-licious returns results under "hits"
    if products:
        return products[0]  # return the first/best match
    return None  # no matches found
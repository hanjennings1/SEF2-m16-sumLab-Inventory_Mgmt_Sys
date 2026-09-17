# Inventory Management System
**Completed Sept 17, 2026**

A Flask-based REST API for managing retail inventory, with CRUD operations, OpenFoodFacts integration for real product data, and a CLI for interacting with the system.

## Features
- Flask REST API with full CRUD support (GET, POST, PATCH, DELETE)
- OpenFoodFacts integration to look up real product data by barcode or name
- Command-line interface (CLI) for managing inventory without a frontend
- Unit tests covering the API, CLI, and external API integration, using pytest and unittest.mock

## Installation and Setup

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd <repo-folder-name>
   ```

2. **Create and activate a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Flask server**
   ```bash
   python app.py
   ```
   The API will be available at `http://127.0.0.1:5000`.

5. **Run the CLI** (in a separate terminal, with the Flask server running)
   ```bash
   python cli.py
   ```

6. **Run the test suite**
   ```bash
   pytest -v
   ```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/inventory` | Get all inventory items |
| GET | `/inventory/<id>` | Get a single item by ID |
| POST | `/inventory` | Add a new item |
| PATCH | `/inventory/<id>` | Update an existing item |
| DELETE | `/inventory/<id>` | Delete an item |

### Example: Add an item (POST)
```json
{
    "product_name": "Chocolate Milk",
    "brands": "Fairlife",
    "ingredients_text": "Ultra-filtered milk, sugar, cocoa processed with alkali",
    "price": 5.99,
    "stock": 25
}
```

### Example: Update an item (PATCH)
```json
{
    "price": 6.49
}
```

## CLI Usage

Run the CLI with:
```bash
python cli.py
```

You'll see a menu:
```
--- Inventory Management CLI ---
1. Add new item
2. View inventory
3. Update item
4. Delete item
5. Find item on OpenFoodFacts
6. Exit
```

- **Add new item**: prompts for product name, brand, ingredients, price, and stock, then adds it to inventory.
- **View inventory**: view all items, or look up one specific item by ID.
- **Update item**: update any field (price, stock, name, brand, or ingredients) on an existing item.
- **Delete item**: remove an item by ID.
- **Find item on OpenFoodFacts**: search the OpenFoodFacts database by barcode or product name (does not automatically add the result to inventory).

## Project Structure
```
├── app.py                    -> Flask app and API routes
├── data.py                   -> Simulated in-memory database and helper functions
├── external_api.py           -> OpenFoodFacts API integration
├── cli.py                    -> Command-line interface
├── tests/
│   ├── test_app.py           -> API endpoint tests
│   ├── test_cli.py           -> CLI tests
│   └── test_external_api.py  -> External API tests (mocked)
├── conftest.py                -> Pytest configuration (path setup)
├── requirements.txt          -> Python dependencies
└── README.md
```

## Notes
- Inventory data is stored in memory (a Python list) and resets each time the Flask server restarts; this is intentional, per the lab's "simulated storage" requirement.
- The CLI's update feature was intentionally expanded to allow editing any field, not just price/stock, for added flexibility beyond the base task requirements.
import requests  # lets us make HTTP requests to our Flask API

BASE_URL = "http://127.0.0.1:5000"  # base address of local Flask server


# --- ADD ITEM ---
# Prompts the user for product details and sends a POST request to create a new item
def add_item():
    product_name = input("Product name: ")
    brands = input("Brand: ")
    ingredients_text = input("Ingredients: ")

    try:
        price = round(float(input("Price: ")), 2)   # round to 2 decimal places (currency format)
        stock = int(input("Stock quantity: "))      # must be a whole number
    except ValueError:
        print("Invalid: Price must be number with two decimals / Stock must be whole number.")
        return  # exit early if conversion fails

    payload = {
        "product_name": product_name,
        "brands": brands,
        "ingredients_text": ingredients_text,
        "price": price,
        "stock": stock
    }

    try:
        response = requests.post(f"{BASE_URL}/inventory", json=payload)  # send data to Flask
        if response.status_code == 201:
            print("Item added:", response.json())
        else:
            print("Error adding item:", response.json())
    except requests.exceptions.ConnectionError:
        print("Cannot Connect: Make Sure Flask is Running")


# --- VIEW INVENTORY ---
# Lets the user view all items, or look up one specific item by ID
def view_inventory():
    print("1. View all items")
    print("2. View a single item")
    choice = input("Choose an option: ")

    try:
        if choice == "1":
            response = requests.get(f"{BASE_URL}/inventory")
            print(response.json())
        elif choice == "2":
            item_id = input("Enter item ID: ")
            response = requests.get(f"{BASE_URL}/inventory/{item_id}")
            if response.status_code == 200:
                print(response.json())
            else:
                print("Item not found.")
        else:
            print("Invalid choice.")
    except requests.exceptions.ConnectionError:
        print("Cannot Connect: Make Sure Flask is Running")


# --- UPDATE ITEM ---
# Lets the user update a specific field (price, stock, name, brand, or ingredients) for an existing item
def update_item():
    item_id = input("Enter item ID to update: ")

    print("1. Price")
    print("2. Stock")
    print("3. Product name")
    print("4. Brand")
    print("5. Ingredients")
    choice = input("Which field would you like to update? ")

    field_map = {
        "1": "price",
        "2": "stock",
        "3": "product_name",
        "4": "brands",
        "5": "ingredients_text"
    }

    field = field_map.get(choice)  # look up the actual field name from the menu choice
    if not field:
        print("Invalid choice.")
        return

    value = input(f"New value for {field}: ")

    # Convert numeric fields to the right type
    if field == "price":
        try:
            value = round(float(value), 2)
        except ValueError:
            print("Price must be a number.")
            return
    elif field == "stock":
        try:
            value = int(value)
        except ValueError:
            print("Stock must be a whole number.")
            return

    payload = {field: value}

    # attempt update, report result or connection error
    try:
        response = requests.patch(f"{BASE_URL}/inventory/{item_id}", json=payload)
        if response.status_code == 200:
            print("Item updated:", response.json())
        else:
            print("Error updating item:", response.json())
    except requests.exceptions.ConnectionError:
        print("Cannot Connect: Make Sure Flask is Running")


# --- DELETE ITEM ---
# Removes an item from the inventory by ID
def delete_item():
    item_id = input("Enter item ID to delete: ")

    # send delete request, handle success/failure
    try:
        response = requests.delete(f"{BASE_URL}/inventory/{item_id}")
        if response.status_code == 200:
            print("Item deleted.")
        else:
            print("Error deleting item:", response.json())
    except requests.exceptions.ConnectionError:
        print("Cannot Connect: Make Sure Flask is Running")


# --- FIND ITEM ON API ---
# Searches OpenFoodFacts by barcode or name, without saving the result to inventory
def find_on_api():
    import external_api  # imported here so the rest of the CLI still works even if this file is missing

    print("1. Search by barcode")
    print("2. Search by name")
    choice = input("Choose an option: ")

    # get the search result based on user's choice:
    if choice == "1":
        barcode = input("Enter barcode: ")
        product = external_api.fetch_by_barcode(barcode)
    elif choice == "2":
        name = input("Enter product name: ")
        product = external_api.fetch_by_name(name)
    else:
        print("Invalid choice.")
        return

    if product:
        print("Found product:")
        print(product)
    else:
        print("No product found.")


# --- MAIN MENU ---
# Runs the CLI loop, letting the user pick an action until they choose to exit
def main_menu():
    while True:
        print("\n--- Inventory Management CLI ---")
        print("1. Add new item")
        print("2. View inventory")
        print("3. Update item")
        print("4. Delete item")
        print("5. Find item on OpenFoodFacts")
        print("6. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            add_item()
        elif choice == "2":
            view_inventory()
        elif choice == "3":
            update_item()
        elif choice == "4":
            delete_item()
        elif choice == "5":
            find_on_api()
        elif choice == "6":
            print("Goodbye!")
            break  # exits the while loop, ending the program
        else:
            print("Invalid option, try again.")


# only runs main_menu() if this file is executed directly (not imported elsewhere)
if __name__ == "__main__":
    main_menu()
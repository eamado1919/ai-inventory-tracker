# AI Inventory Tracker
# Stores inventory items, calculates inventory value,
# tracks stock status, supports item search, and updates quantities.

import csv
from pathlib import Path
from datetime import datetime


# --------------------------------------------------
# CREATE EMPTY INVENTORY LIST
# --------------------------------------------------
inventory = []


# --------------------------------------------------
# ADD A NEW INVENTORY ITEM
# --------------------------------------------------
def add_item(item_id, name, quantity, price):

    # Create one inventory record
    item = {
        "item_id": item_id,
        "name": name,
        "quantity": quantity,
        "price": price,

        # Record when the item was added
        "created_at": datetime.now().strftime(
            "%m/%d/%Y %I:%M:%S %p"
        )
    }

    # Add the new item to the inventory list
    inventory.append(item)

    # Return the new record
    return item


# --------------------------------------------------
# DETERMINE STOCK STATUS
# --------------------------------------------------
def get_stock_status(quantity):

    if quantity == 0:
        return "OUT OF STOCK"

    elif quantity <= 5:
        return "LOW STOCK"

    else:
        return "IN STOCK"


# --------------------------------------------------
# FIND ITEM BY ID
# --------------------------------------------------
def find_item_by_id(item_id):

    # Search each inventory record
    for item in inventory:

        # Return the matching item
        if item["item_id"] == item_id:
            return item

    # Return None if no match is found
    return None


# --------------------------------------------------
# UPDATE ITEM QUANTITY
# --------------------------------------------------
def update_quantity(item_id, new_quantity):

    # Find the existing item
    item = find_item_by_id(item_id)

    # Stop if the item does not exist
    if item is None:
        return None

    # Do not allow negative inventory
    if new_quantity < 0:
        return None

    # Update the quantity
    item["quantity"] = new_quantity

    # Return the updated record
    return item


# --------------------------------------------------
# CREATE INVENTORY SUMMARY
# --------------------------------------------------
def get_inventory_summary():

    # Start summary counters
    total_records = len(inventory)
    total_quantity = 0
    total_value = 0
    out_of_stock_count = 0
    low_stock_count = 0

    # Review every inventory item
    for item in inventory:

        quantity = item["quantity"]
        price = item["price"]

        # Add quantity to total quantity
        total_quantity += quantity

        # Add item value to total inventory value
        total_value += quantity * price

        # Determine current stock status
        stock_status = get_stock_status(quantity)

        if stock_status == "OUT OF STOCK":
            out_of_stock_count += 1

        elif stock_status == "LOW STOCK":
            low_stock_count += 1

    # Return summary data
    return {
        "total_records": total_records,
        "total_quantity": total_quantity,
        "total_value": total_value,
        "out_of_stock_count": out_of_stock_count,
        "low_stock_count": low_stock_count
    }


# --------------------------------------------------
# EXPORT INVENTORY REPORT
# --------------------------------------------------

def export_inventory_snapshot():

    # Save the CSV file in the same folder as this Python script
    output_path = Path(__file__).resolve().parent / "inventory_snapshot.csv"

    # Define the columns in the report
    headers = [
        "item_id",
        "name",
        "quantity",
        "price",
        "inventory_value",
        "stock_status",
        "created_at"
    ]

    # Open the file for writing
    with output_path.open("w", newline="", encoding="utf-8") as file:

        # Create a CSV writer
        writer = csv.DictWriter(file, fieldnames=headers)

        # Write the column headings
        writer.writeheader()

        # Process every inventory record
        for item in inventory:

            # Calculate the inventory value
            inventory_value = item["quantity"] * item["price"]

            # Determine the item's current stock status
            stock_status = get_stock_status(item["quantity"])

            # Write the item information to the CSV file
            writer.writerow({
                "item_id": item["item_id"],
                "name": item["name"],
                "quantity": item["quantity"],
                "price": f"{item['price']:.2f}",
                "inventory_value": f"{inventory_value:.2f}",
                "stock_status": stock_status,
                "created_at": item["created_at"]
            })

    # Return the location of the completed report
    return output_path


# --------------------------------------------------
# ADD SAMPLE INVENTORY ITEMS
# --------------------------------------------------
add_item("ITEM-1001", "Laptop", 100, 899.99)
add_item("ITEM-1002", "Wireless Mouse", 25, 29.99)
add_item("ITEM-1003", "Keyboard", 12, 49.99)
add_item("ITEM-1004", "Monitor", 0, 249.99)
add_item("ITEM-1005", "Webcam", 7, 79.99)


# --------------------------------------------------
# UPDATE EXISTING INVENTORY
# --------------------------------------------------

# Simulate receiving new Monitor inventory
updated_item = update_quantity("ITEM-1004", 15)


# --------------------------------------------------
# SEARCH FOR A SPECIFIC ITEM
# --------------------------------------------------
search_result = find_item_by_id("ITEM-1003")



# --------------------------------------------------
# AUTOMATED INVENTORY TESTING
# --------------------------------------------------

print("\n--- INVENTORY VALIDATION TESTS ---")

# TEST 1: Verify the correct number of inventory records
assert len(inventory) == 5, "Inventory record count is incorrect"


# TEST 2: Verify there are no duplicate item IDs
item_ids = [item["item_id"] for item in inventory]

assert len(item_ids) == len(set(item_ids)), "Duplicate Item IDs found"


# TEST 3: Verify the Monitor quantity was updated correctly
monitor = find_item_by_id("ITEM-1004")

assert monitor is not None, "Monitor was not found"

assert monitor["quantity"] == 15, "Monitor quantity is incorrect"


# TEST 4: Verify negative inventory quantities are rejected
result = update_quantity("ITEM-1004", -5)

assert result is None, "Negative quantity was accepted"

assert monitor["quantity"] == 15, "Rejected update changed inventory"


# TEST 5: Verify the inventory summary
test_summary = get_inventory_summary()

assert test_summary["total_records"] == 5
assert test_summary["total_quantity"] == 159
assert round(test_summary["total_value"], 2) == 95658.41
assert test_summary["out_of_stock_count"] == 0
assert test_summary["low_stock_count"] == 0


# TEST 6: Verify an invalid item ID is handled correctly
result = find_item_by_id("ITEM-9999")

assert result is None, "Invalid item ID was found"


print("All inventory validation tests passed!")


# --------------------------------------------------
# DISPLAY INVENTORY ITEMS
# --------------------------------------------------
print("\n--- INVENTORY ITEMS ---")

for item in inventory:

    # Calculate value for the current item
    inventory_value = item["quantity"] * item["price"]

    # Determine current stock status
    stock_status = get_stock_status(item["quantity"])

    # Display item information
    print(f"\nItem ID: {item['item_id']}")
    print(f"Name: {item['name']}")
    print(f"Quantity: {item['quantity']}")
    print(f"Price: ${item['price']:,.2f}")
    print(f"Inventory Value: ${inventory_value:,.2f}")
    print(f"Created At: {item['created_at']}")
    print(f"Stock Status: {stock_status}")


# --------------------------------------------------
# DISPLAY INVENTORY SUMMARY
# --------------------------------------------------
summary = get_inventory_summary()

print("\n--- INVENTORY SUMMARY ---")

print(f"Total Records: {summary['total_records']}")
print(f"Total Quantity: {summary['total_quantity']}")
print(f"Total Inventory Value: ${summary['total_value']:,.2f}")
print(f"Out of Stock: {summary['out_of_stock_count']}")
print(f"Low Stock: {summary['low_stock_count']}")


# --------------------------------------------------
# DISPLAY ITEM SEARCH RESULT
# --------------------------------------------------
print("\n--- ITEM SEARCH ---")

if search_result:

    print(f"Item ID: {search_result['item_id']}")
    print(f"Name: {search_result['name']}")
    print(f"Quantity: {search_result['quantity']}")
    print(f"Price: ${search_result['price']:,.2f}")

else:

    print("Item not found.")


# --------------------------------------------------
# DISPLAY RESTOCK LIST
# --------------------------------------------------
print("\n--- RESTOCK LIST ---")

restock_found = False

for item in inventory:

    stock_status = get_stock_status(item["quantity"])

    # Display items needing attention
    if stock_status == "OUT OF STOCK" or stock_status == "LOW STOCK":

        print(
            f"{item['item_id']} - "
            f"{item['name']} - "
            f"Quantity: {item['quantity']}"
        )

        restock_found = True


# If no inventory needs restocking
if not restock_found:
    print("No items currently need restocking.")

    # --------------------------------------------------
# CREATE AND VERIFY FINAL INVENTORY REPORT
# --------------------------------------------------

print("\n--- INVENTORY EXPORT ---")

# Generate the report
snapshot_path = export_inventory_snapshot()

# Read the report back into Python
with snapshot_path.open("r", newline="", encoding="utf-8") as file:
    exported_records = list(csv.DictReader(file))

# Verify that all inventory records were exported
assert len(exported_records) == len(inventory)

# Verify that the report is not empty
assert len(exported_records) > 0

print(f"Inventory report created: {snapshot_path.name}")
print(f"Records exported: {len(exported_records)}")
print("Inventory export validation passed!")

# --------------------------------------------------
# FINAL INVENTORY DATA VALIDATION
# --------------------------------------------------

def validate_inventory_before_export():

    # Track item IDs to detect duplicates
    seen_ids = set()

    # Review every inventory record
    for item in inventory:

        item_id = item["item_id"]

        # Check for duplicate records
        if item_id in seen_ids:
            raise ValueError(f"Duplicate Item ID: {item_id}")

        # Record the item ID as reviewed
        seen_ids.add(item_id)

        # Validate quantity
        if not isinstance(item["quantity"], int) or item["quantity"] < 0:
            raise ValueError(f"Invalid quantity for {item_id}")

        # Validate price
        if not isinstance(item["price"], (int, float)) or item["price"] < 0:
            raise ValueError(f"Invalid price for {item_id}")

    # All records passed the checks
    print("\nInventory data validation passed!")
    print(f"Unique inventory records validated: {len(seen_ids)}")
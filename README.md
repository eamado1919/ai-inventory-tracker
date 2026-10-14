# AI Inventory Tracker

## Project Overview

AI Inventory Tracker is a Python application that demonstrates inventory tracking, inventory valuation, stock monitoring, quantity updates, searching, validation, and CSV reporting.

## Features

- Create inventory records
- Add timestamps to inventory items
- Calculate inventory value
- Classify items as IN STOCK, LOW STOCK, or OUT OF STOCK
- Search for inventory items by ID
- Update inventory quantities
- Generate inventory summary reports
- Identify items requiring restocking
- Export inventory data to CSV
- Validate inventory records and exported results

## Technologies Used

- Python
- CSV
- datetime
- pathlib
- Git
- GitHub

## Business Rules

- OUT OF STOCK: quantity = 0
- LOW STOCK: quantity between 1 and 5
- IN STOCK: quantity greater than 5
- Negative quantities are rejected

## Sample Products

The sample application includes:

- Laptop
- Wireless Mouse
- Keyboard
- Monitor
- Webcam

## How to Run

From the `PythonPractice` directory:

```powershell
python .\ai-inventory-tracker\ai_inventory_tracker.py

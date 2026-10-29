import csv

expenses = [
    {"amount": 250.0, "category": "food", "note": "Lunch"},
    {"amount": 80.5, "category": "travel", "note": "Auto ride"},
    {"amount": 120.0, "category": "food", "note": "Dinner"},
]

with open("expenses.csv", "w", newline="", encoding="utf-8") as file:
    fields = ["amount", "category", "note"]
    writer = csv.DictWriter(file, fieldnames=fields)
    writer.writeheader()
    writer.writerows(expenses)

import csv

expenses = [
    {"amount": 250.0, "category": "food", "note": "Lunch"},
    {"amount": 80.5, "category": "travel", "note": "Auto ride"},
    {"amount": 120.0, "category": "food", "note": "Dinner"},
]

with open("expenses.csv", newline="", encoding="utf-8") as file:
    loaded = list(csv.DictReader(file))

for e in loaded:
    e["amount"] = float(e["amount"])

print(loaded[0])
print(loaded == expenses)

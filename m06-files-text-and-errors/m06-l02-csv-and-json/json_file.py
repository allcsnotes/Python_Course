import json

expenses = [
    {"amount": 250.0, "category": "food", "note": "Lunch"},
    {"amount": 80.5, "category": "travel", "note": "Auto ride"},
    {"amount": 120.0, "category": "food", "note": "Dinner"},
]

with open("expenses.json", "w", encoding="utf-8") as file:
    json.dump(expenses, file, indent=2)

with open("expenses.json", encoding="utf-8") as file:
    loaded = json.load(file)

print(loaded == expenses)
print(loaded[1]["amount"] + 1)

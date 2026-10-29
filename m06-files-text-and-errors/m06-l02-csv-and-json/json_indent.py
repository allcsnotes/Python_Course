import json

expense = {"amount": 250.0, "category": "food", "note": "Lunch"}
print(json.dumps(expense))
print(json.dumps(expense, indent=2))

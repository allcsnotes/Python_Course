import json
from pathlib import Path

path = Path("expenses.json")


def save_expenses(expenses):
    with open(path, "w", encoding="utf-8") as file:
        json.dump(expenses, file, indent=2)


def load_expenses():
    if not path.exists():
        return []
    with open(path, encoding="utf-8") as file:
        return json.load(file)


expenses = load_expenses()
print("Loaded:", len(expenses))

amount = float(input("Amount: "))
category = input("Category: ").lower()
note = input("Note: ")
expenses.append({"amount": amount, "category": category, "note": note})

save_expenses(expenses)
print("Saved:", len(expenses))

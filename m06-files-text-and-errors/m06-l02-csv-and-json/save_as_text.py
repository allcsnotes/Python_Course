expense = {"amount": 250.0, "category": "food", "note": "Lunch"}
with open("expense.txt", "w", encoding="utf-8") as file:
    file.write(str(expense))
with open("expense.txt", encoding="utf-8") as file:
    back = file.read()
print(back)
print(type(back))
print(back["note"])

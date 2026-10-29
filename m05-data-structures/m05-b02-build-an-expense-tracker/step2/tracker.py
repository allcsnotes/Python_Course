def add_expense(expenses):
    amount = float(input("Amount: "))
    category = input("Category: ").strip().lower()
    note = input("Note: ").strip()
    expense = {
        "amount": amount,
        "category": category,
        "note": note,
    }
    expenses.append(expense)
    print("Saved.")


expenses = []
add_expense(expenses)
add_expense(expenses)
print(expenses)

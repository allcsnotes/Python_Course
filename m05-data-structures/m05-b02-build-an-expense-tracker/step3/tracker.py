def show_expenses(expenses):
    if not expenses:
        print("No expenses yet.")
        return
    print(f"{'Category':<12}{'Note':<18}{'Amount':>10}")
    print("-" * 40)
    for e in expenses:
        cat, note, amt = e["category"], e["note"], e["amount"]
        print(f"{cat:<12}{note:<18}{amt:>10.2f}")


expenses = [
    {"amount": 250.0, "category": "food", "note": "lunch"},
    {"amount": 80.5, "category": "travel", "note": "auto ride"},
    {"amount": 1499.0, "category": "learning", "note": "course"},
    {"amount": 120.0, "category": "food", "note": "dinner"},
]
show_expenses(expenses)
show_expenses([])

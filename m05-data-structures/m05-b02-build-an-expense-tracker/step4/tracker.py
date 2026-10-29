def totals_by_category(expenses):
    totals = {}
    for e in expenses:
        cat = e["category"]
        totals[cat] = totals.get(cat, 0) + e["amount"]
    return totals


def show_totals(expenses):
    if not expenses:
        print("No expenses yet.")
        return
    print(f"{'Category':<12}{'Total':>10}")
    print("-" * 22)
    grand = 0
    for cat, total in totals_by_category(expenses).items():
        print(f"{cat:<12}{total:>10.2f}")
        grand += total
    print("-" * 22)
    print(f"{'All':<12}{grand:>10.2f}")
    used = {e["category"] for e in expenses}
    print(f"{len(used)} categories used")


expenses = [
    {"amount": 250.0, "category": "food", "note": "lunch"},
    {"amount": 80.5, "category": "travel", "note": "auto ride"},
    {"amount": 1499.0, "category": "learning", "note": "course"},
    {"amount": 120.0, "category": "food", "note": "dinner"},
]
print(totals_by_category(expenses))
show_totals(expenses)

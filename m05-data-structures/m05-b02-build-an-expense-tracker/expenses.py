def show_menu():
    print()
    print("1 Add   2 List   3 Totals   4 Quit")


def ask_text(question):
    while True:
        text = input(question).strip()
        if text:
            return text
        print("Please type something.")


def ask_amount():
    while True:
        text = input("Amount: ").strip()
        if not text.replace(".", "", 1).isdigit():
            print("Please type a number, like 250 or 80.5.")
            continue
        amount = float(text)
        if amount <= 0:
            print("The amount must be more than zero.")
            continue
        return amount


def add_expense(expenses):
    amount = ask_amount()
    category = ask_text("Category: ").lower()
    note = ask_text("Note: ")
    expense = {
        "amount": amount,
        "category": category,
        "note": note,
    }
    expenses.append(expense)
    print("Saved.")


def show_expenses(expenses):
    if not expenses:
        print("No expenses yet.")
        return
    print(f"{'Category':<12}{'Note':<18}{'Amount':>10}")
    print("-" * 40)
    for e in expenses:
        cat, note, amt = e["category"], e["note"], e["amount"]
        note = note[:18]
        print(f"{cat:<12}{note:<18}{amt:>10.2f}")


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


def main():
    expenses = []
    while True:
        show_menu()
        choice = input("Choose: ").strip()
        match choice:
            case "1":
                add_expense(expenses)
            case "2":
                show_expenses(expenses)
            case "3":
                show_totals(expenses)
            case "4" | "q":
                print("Goodbye!")
                break
            case _:
                print("Please choose 1, 2, 3 or 4.")


main()

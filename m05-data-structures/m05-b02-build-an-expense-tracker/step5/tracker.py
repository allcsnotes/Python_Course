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


expenses = []
add_expense(expenses)
print(expenses)

def make_expense(amount, category):
    if amount <= 0:
        raise ValueError("amount must be positive")
    return {"amount": amount, "category": category}


def save_expense(text):
    try:
        expense = make_expense(float(text), "food")
        print("Saved:", expense["amount"])
    except ValueError as error:
        print("Could not save:", error)


save_expense("250")
save_expense("-50")
save_expense("abc")

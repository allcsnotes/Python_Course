def make_expense(amount, category):
    if amount <= 0:
        raise ValueError("amount must be positive")
    return {"amount": amount, "category": category}


print(make_expense(250, "food"))
print(make_expense(-50, "food"))

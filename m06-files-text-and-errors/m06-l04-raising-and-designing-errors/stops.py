def check(amount):
    if amount <= 0:
        raise ValueError("amount must be positive")
    print("amount is fine")


check(50)
check(-50)

def ask_amount():
    while True:
        text = input("Amount: ").strip()
        try:
            amount = float(text)
        except ValueError:
            print("Please type a number like 250 or 80.5")
        else:
            return amount


print("Saved", ask_amount())

text = input("Amount: ").strip()
try:
    amount = float(text)
except ValueError:
    print("Please type a number like 250 or 80.5")
else:
    print("Saved", amount)

text = input("Amount: ").strip()
if text.replace(".", "", 1).isdigit():
    amount = float(text)
    print("Saved", amount)
else:
    print("Please type a number like 250 or 80.5")

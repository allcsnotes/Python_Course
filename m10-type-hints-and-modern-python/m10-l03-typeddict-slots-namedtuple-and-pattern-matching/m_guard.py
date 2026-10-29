def pay(command):
    match command:
        case ["pay", amount] if amount >= 5000:
            return "needs approval"
        case ["pay", amount] if amount > 0:
            return f"paid {amount}"
        case ["pay", _]:
            return "invalid amount"
        case _:
            return "unknown command"


print(pay(["pay", 9999]))
print(pay(["pay", 1499]))
print(pay(["pay", -5]))

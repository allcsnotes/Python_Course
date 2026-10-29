prices = {"Python": 1499, "SQL": 999, "Docker": 799}
del prices["Docker"]
print(prices)
old = prices.pop("SQL")
print(old)
print(prices)

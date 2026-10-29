prices = {"Python": 1499, "SQL": 999, "Docker": 799}
print(prices.get("SQL"))
print(prices.get("Java"))
print(prices.get("Java", 0))

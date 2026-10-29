# Exercise 10 - Predict the output (dictionaries)
prices = {"Python": 1499, "SQL": 999, "Docker": 799}
print(prices["SQL"])
print(prices.get("Docker"), prices.get("Go"), prices.get("Go", 0))
print("SQL" in prices, 999 in prices, "Go" not in prices)
prices["SQL"] = 899
prices["Go"] = 699
print(prices)
print(prices.pop("Python"))
print(len(prices))
del prices["Go"]
print(prices)
for course, price in prices.items():
    print(course, "->", price)
for price in prices.values():
    print(price)
for key in prices:
    print(key)
nested = {"Asha": {"marks": [80, 90]}}
print(nested["Asha"]["marks"][-1])
counts = {}
counts["a"] = counts.get("a", 0) + 1
counts["a"] = counts.get("a", 0) + 1
print(counts)

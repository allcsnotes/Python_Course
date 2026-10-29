prices = [1499, 999, 1999]
cheap = [price if price < 1500 else 0 for price in prices]
print(cheap)

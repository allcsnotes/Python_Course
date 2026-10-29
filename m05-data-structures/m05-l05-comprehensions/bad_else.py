prices = [1499, 999, 1999]
cheap = [price for price in prices if price < 1500 else 0]
print(cheap)

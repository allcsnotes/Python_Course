prices = [1499, 999, 1999, 499, 2499]
cheap = []
for price in prices:
    if price < 1500:
        cheap.append(price)
print(cheap)

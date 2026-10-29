prices = [1499, 0, 1999, 499]
labels = [
    "free" if price == 0 else "cheap" if price < 1500
    else "pricey" for price in prices
]
print(labels)

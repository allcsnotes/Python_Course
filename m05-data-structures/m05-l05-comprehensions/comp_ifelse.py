prices = [1499, 999, 1999, 499, 2499]
labels = [
    "cheap" if price < 1500 else "pricey"
    for price in prices
]
print(labels)

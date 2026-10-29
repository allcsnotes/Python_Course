prices = [1499, 0, 1999, 499]
labels = []
for price in prices:
    if price == 0:
        labels.append("free")
    elif price < 1500:
        labels.append("cheap")
    else:
        labels.append("pricey")
print(labels)

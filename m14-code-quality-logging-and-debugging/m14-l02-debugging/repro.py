total = 0
for price in [1500, 500]:
    total = total + price
    total = total - total * 10 / 100
print(total)

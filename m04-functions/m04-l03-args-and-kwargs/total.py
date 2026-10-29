def total_price(*prices):
    total = 0
    for price in prices:
        total += price
    return total

print(total_price(1499, 999))
print(total_price(1499, 999, 1999, 499))
print(total_price())

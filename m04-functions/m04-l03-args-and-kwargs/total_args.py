def total_price(*args):
    total = 0
    for price in args:
        total += price
    return total

print(total_price(1499, 999))

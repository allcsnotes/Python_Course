def total_price(*prices):
    total = 0
    for price in prices:
        total += price
    return total

basket = [1499, 999, 1999]
print(total_price(*basket))

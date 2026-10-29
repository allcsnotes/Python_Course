def min_max(prices):
    return min(prices), max(prices)

low, high = min_max((1499, 999, 1999))
print(low, high)
first, *rest = (1499, 999, 1999)
print(first, rest)

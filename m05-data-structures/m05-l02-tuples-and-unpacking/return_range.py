def price_range(prices):
    return min(prices), max(prices)

low, high = price_range((1499, 999, 1999, 499))
print(low, high)

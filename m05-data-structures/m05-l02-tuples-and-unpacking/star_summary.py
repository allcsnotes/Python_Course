def show(*prices):
    print(prices)

show(1, 2)
prices = (1, 2, 3)
print(*prices)
first, *rest = prices
print(rest)

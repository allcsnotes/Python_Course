from functools import cache


@cache
def total(prices):
    return sum(prices)


print(total([499, 999]))

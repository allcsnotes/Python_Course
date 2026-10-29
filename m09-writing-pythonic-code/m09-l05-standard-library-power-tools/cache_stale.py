from functools import cache

rate = 1.18


@cache
def with_tax(price):
    return price * rate


print(with_tax(2000))
rate = 1.05
print(with_tax(2000))

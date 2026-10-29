from functools import partial


def price_after(price, discount):
    return price - price * discount / 100


festive = partial(price_after, discount=20)
print(price_after(2000, 20))
print(festive(2000))
print(festive(500))

import random


def lucky_price(price):
    percent = random.choice([0, 10, 25, 50])
    return price - price * percent // 100

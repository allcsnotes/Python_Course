def convert_price(text):
    return int(text)


def add_price(total, text):
    return total + convert_price(text)


def checkout(prices):
    total = 0
    for text in prices:
        total = add_price(total, text)
    return total


print(checkout(["1499", "999", "abc"]))

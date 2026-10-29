from discounts import student


def cart_total(prices, rule):
    return sum(rule(price) for price in prices)


print(cart_total([1000, 500], student))
print(cart_total([1000, 500], lambda price: price - 100))

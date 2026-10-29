def price_after_coupon(price, percent):
    return price - price * percent / 100


def cart_total(prices, percent):
    total = 0
    for price in prices:
        breakpoint()
        total = total + price
        total = price_after_coupon(total, percent)
    return total


if __name__ == "__main__":
    prices = [1500, 500, 500]
    print(cart_total(prices, 10))

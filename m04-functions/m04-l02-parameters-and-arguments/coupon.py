def apply_coupon(price):
    price = price - 100
    return price

price = 1000
new_price = apply_coupon(price)
print(price, new_price)

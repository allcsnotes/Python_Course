def sale_price(price, percent):
    return price - price * percent / 100

print(sale_price(price=1000, percent=20))
print(sale_price(percent=20, price=1000))
print(sale_price(1000, percent=20))

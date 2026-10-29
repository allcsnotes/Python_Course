def sale_price(price, percent=10):
    return price - price * percent / 100

print(sale_price(1000))
print(sale_price(1000, 25))
print(sale_price(1000, percent=50))

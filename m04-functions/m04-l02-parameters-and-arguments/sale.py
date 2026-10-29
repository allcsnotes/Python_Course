def sale_price(price, percent):
    return price - price * percent / 100

print(sale_price(1000, 20))
print(sale_price(500, 10))

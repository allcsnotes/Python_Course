def split_price(amount):
    return amount // 100, amount % 100

result = split_price(235882)
print(result)
print(type(result))
rupees, paise = split_price(235882)
print(rupees, paise)

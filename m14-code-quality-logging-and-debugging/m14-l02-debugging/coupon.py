COUPONS = {"SAVE10": 10, "SAVE20": 20}


def percent_for(code):
    return COUPONS[code]


def checkout(price, code):
    percent = percent_for(code)
    return price - price * percent / 100


print(checkout(2500, "SAVE10"))
print(checkout(2500, "save20"))

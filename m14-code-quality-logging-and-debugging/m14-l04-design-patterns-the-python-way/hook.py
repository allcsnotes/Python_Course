def final_price(price, kind):
    if kind == "student":
        return price * 80 // 100
    elif kind == "festival":
        return price * 90 // 100
    elif kind == "bulk":
        return price * 85 // 100
    return price


print(final_price(1000, "student"))
print(final_price(1000, "studnet"))

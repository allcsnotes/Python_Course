def apply_discount(price, percent):
    final = price - price * percent / 100
    assert 0 <= final <= price, "bad final price"
    return final


print(apply_discount(1000, 20))
print(apply_discount(1000, 150))

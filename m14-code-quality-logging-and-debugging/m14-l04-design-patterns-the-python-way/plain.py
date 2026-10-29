def student(price):
    return price * 80 // 100


def total(price, discount):
    return discount(price)


print(total(1000, student))

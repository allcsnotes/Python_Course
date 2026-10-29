def student(price):
    return price * 80 // 100


def festival(price):
    return price * 90 // 100


def bulk(price):
    return price * 85 // 100


DISCOUNTS = {
    "student": student,
    "festival": festival,
    "bulk": bulk,
}


def final_price(price, kind):
    return DISCOUNTS[kind](price)

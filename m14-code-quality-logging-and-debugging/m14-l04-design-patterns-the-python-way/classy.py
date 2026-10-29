class StudentDiscount:
    def apply(self, price):
        return price * 80 // 100


class Checkout:
    def __init__(self, discount):
        self.discount = discount

    def total(self, price):
        return self.discount.apply(price)


print(Checkout(StudentDiscount()).total(1000))

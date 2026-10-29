class Plain:
    def __init__(self, price):
        self.price = price


class Slim:
    __slots__ = ("price",)

    def __init__(self, price):
        self.price = price


a = Plain(100)
a.pirce = 90
print(a.__dict__)
b = Slim(100)
b.pirce = 90

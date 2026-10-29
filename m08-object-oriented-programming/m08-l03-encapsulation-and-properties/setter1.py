class Course:
    def __init__(self, title, price):
        self.title = title
        self.price = price

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        if value < 0:
            raise ValueError(f"price cannot be negative, got {value}")
        self._price = value


course = Course("Python", 499)
course.price = 599
print(course.price)
course.price = -500

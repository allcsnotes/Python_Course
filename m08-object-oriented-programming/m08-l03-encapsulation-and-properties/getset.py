class Course:
    def __init__(self, title, price):
        self.title = title
        self._price = price

    def get_price(self):
        return self._price

    def set_price(self, value):
        if value < 0:
            raise ValueError("price cannot be negative")
        self._price = value


course = Course("Python", 499)
course.set_price(course.get_price() + 100)
print(course.get_price())
course.set_price(-500)

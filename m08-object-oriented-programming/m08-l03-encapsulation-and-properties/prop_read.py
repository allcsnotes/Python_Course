class Course:
    def __init__(self, title, price):
        self.title = title
        self._price = price

    @property
    def price(self):
        return self._price


course = Course("Python", 499)
print(course.price)
course.price = 399

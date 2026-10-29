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


def apply_sale(course):
    course.price = course.price - 100


course = Course("Python", 499)
apply_sale(course)
print(course.price)
quiz = Course("Quiz Pack", 50)
apply_sale(quiz)

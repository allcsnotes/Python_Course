class Course:
    def __init__(self, title, price):
        self.title = title
        self.price = price


def apply_sale(course):
    course.price = course.price - 100


course = Course("Python", 499)
apply_sale(course)
print(course.price)

class Course:
    def __init__(self, title, price):
        self.title = title
        self.price = price

    def price_after(self, percent):
        return self.price * (100 - percent) // 100

    def apply_discount(self, percent):
        self.price = self.price_after(percent)


python_course = Course("Python", 499)
print(python_course.price_after(10), python_course.price)
python_course.apply_discount(10)
print(python_course.price)

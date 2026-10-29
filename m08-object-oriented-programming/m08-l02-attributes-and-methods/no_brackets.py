class Course:
    def __init__(self, title, price):
        self.title = title
        self.price = price

    def describe(self):
        return self.title.upper()


python_course = Course("Python", 499)
print(python_course.describe)

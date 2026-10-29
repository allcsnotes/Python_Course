class Course:
    def __init__(self, title, price):
        self.title = title
        self.price = price

    def describe(self):
        return f"{self.title} costs Rs {self.price}"


python_course = Course("Python", 499)
print(python_course.describe())
print(Course.describe(python_course))

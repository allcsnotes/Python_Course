class Course:
    def __init__(self, title, price):
        title = title
        self.price = price


python_course = Course("Python", 499)
print(python_course.price)
print(python_course.title)

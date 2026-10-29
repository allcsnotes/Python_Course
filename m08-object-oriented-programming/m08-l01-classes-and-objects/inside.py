class Course:
    def __init__(self, title, price):
        self.title = title
        self.price = price


python_course = Course("Python", 499)
print(type(python_course))
print(type(python_course) is Course)
print(vars(python_course))

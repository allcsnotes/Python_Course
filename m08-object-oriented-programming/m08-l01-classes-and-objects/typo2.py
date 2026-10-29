class Course:
    def __init__(self, title, price):
        self.title = title
        self.price = price


python_course = Course("Python", 499)
python_course.pricee = 399
print(python_course.price)

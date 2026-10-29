class Course:
    def __init__(self, title, price):
        self.title = title
        self.price = price


course = Course("Python", 499)
course.price = -500
print("Two seats:", course.price * 2)

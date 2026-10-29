class Course:
    def __init__(self, title, price):
        self.title = title
        self._price = price


course = Course("Python", 499)
print(course._price)
course._price = 399
print(course._price)

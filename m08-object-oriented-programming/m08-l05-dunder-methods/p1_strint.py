class Course:
    def __init__(self, price):
        self.price = price

    def __str__(self):
        return self.price


print(Course(499))

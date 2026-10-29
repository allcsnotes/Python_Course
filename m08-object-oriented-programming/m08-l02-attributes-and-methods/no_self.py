class Course:
    def __init__(self, title, price):
        self.title = title
        self.price = price

    def is_free(self):
        return price == 0


print(Course("Python", 499).is_free())

class Course:
    def __init__(self, title, price):
        self.title = title
        self._price = price

    @property
    def is_free(self):
        return self._price == 0


paid = Course("Python", 499)
free = Course("Intro to Python", 0)
print(paid.is_free)
print(free.is_free)

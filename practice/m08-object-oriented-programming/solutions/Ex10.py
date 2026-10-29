# Exercise 10 - Fix the broken property code (all four repaired)
class Course:
    def __init__(self, title, price):
        self.title = title
        self.price = price

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        if value < 0:
            raise ValueError(f"price cannot be negative, got {value}")
        self._price = value             # was: self.price = value  (calls itself forever)


course = Course("Python", 499)
print(course.price)                     # was: course.price()  (no brackets on a property)

course.price = 399                      # was a crash in a version with no setter
print(course.price)

try:
    course.price = -500                 # was: course._price = -500  (skips the check)
except ValueError as error:
    print("Rejected:", error)
print(course.price)

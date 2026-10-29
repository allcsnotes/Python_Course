# Exercise 14 - Predict the output (__str__ and __repr__)
class Course:
    def __init__(self, title, price):
        self.title = title
        self.price = price

    def __str__(self):
        return f"{self.title} (Rs {self.price})"

    def __repr__(self):
        return f"Course({self.title!r}, {self.price})"


class Lesson:
    def __init__(self, title, minutes):
        self.title = title
        self.minutes = minutes

    def __repr__(self):
        return f"Lesson({self.title!r}, {self.minutes})"


course = Course("Python Basics", 499)
lesson = Lesson("Loops", 18)
print(course)
print(repr(course))
print([course])
print(f"Now watching: {course}")
print(f"{course!r}")
print(lesson)
print(str(lesson))
print([lesson, lesson])
print("Lesson:", lesson)

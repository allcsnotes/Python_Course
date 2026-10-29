# Exercise 03 - Fix the broken class code (all five repaired)
class Course:
    def __init__(self, title, price):
        self.title = title              # was: title = title  (no self.)
        self.price = price


course = Course("Python", 499)
print(course.title)

sql = Course("SQL", 399)                # was: Course("SQL")  (price missing)
print(sql.title, sql.price)


class Lesson:
    def __init__(self, title, minutes): # was: def __init__(title, minutes)  (no self)
        self.title = title
        self.minutes = minutes


lesson = Lesson("Variables", 12)
print(lesson.title, lesson.minutes)

print(course.price)                     # was: course.pricee  (typo)

course.price = 399                      # was: course.pricee = 399  (made a new attribute)
print(course.price)

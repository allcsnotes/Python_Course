# Exercise 13 - Fix the broken inheritance code (all three repaired)
class Person:
    def __init__(self, name):
        self.name = name


class Student(Person):
    def __init__(self, name, email):
        super().__init__(name)          # was: missing, so self.name was never set
        self.email = email


priya = Student("Priya", "priya@example.com")
print(priya.email)
print(priya.name)


class Instructor(Person):
    def __init__(self, name, subject):
        super().__init__(name)          # was: super().__init__()  (name not passed up)
        self.subject = subject


meera = Instructor("Meera", "Python")
print(meera.name, meera.subject)


class Lesson:
    def __init__(self, title, minutes):
        self.title = title
        self.minutes = minutes


class Course:                           # was: class Course(Lesson)  (a course is not a lesson)
    def __init__(self, title):
        self.title = title
        self.lessons = []

    def add(self, lesson):
        self.lessons.append(lesson)

    def total_minutes(self):
        total = 0
        for lesson in self.lessons:
            total += lesson.minutes
        return total


basics = Course("Python Basics")
basics.add(Lesson("Variables", 12))
basics.add(Lesson("Loops", 18))
print(isinstance(basics, Lesson))
print(basics.total_minutes())

from domain import AlreadyEnrolledError
from domain import Course, Level, Student

course = Course("Python Basics", 499, Level.BEGINNER)
course.add_lesson("Variables", 12)
course.add_lesson("Loops", 15)
course.add_lesson("Functions", 18)
first, second, third = course.lessons

priya = Student("Priya", "priya@example.com")
enrollment = course.enrol(priya)
print(enrollment.progress)

enrollment.complete(first)
print(enrollment.progress)
enrollment.complete(first)
print(enrollment.progress)
enrollment.complete(second)
enrollment.complete(third)
print(enrollment.progress, enrollment.finished)

try:
    course.enrol(priya)
except AlreadyEnrolledError as err:
    print("refused:", err)

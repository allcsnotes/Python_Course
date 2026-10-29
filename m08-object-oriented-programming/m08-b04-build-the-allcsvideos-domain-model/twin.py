from domain import AlreadyEnrolledError
from domain import Course, Level, Student

course = Course("Python Basics", 499, Level.BEGINNER)
course.enrol(Student("Priya", "priya@example.com"))

twin = Student("Priya R", "priya@example.com")
print(twin == Student("Priya", "priya@example.com"))
try:
    course.enrol(twin)
except AlreadyEnrolledError as err:
    print("Refused:", err)

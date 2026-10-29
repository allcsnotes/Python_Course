from domain import Course, Lesson, Level, Student
from domain import UnknownLessonError

course = Course("Python Basics", 499, Level.BEGINNER)
course.add_lesson("Variables", 12)
lukas = Student("Lukas", "lukas@example.com")
enrollment = course.enrol(lukas)

try:
    enrollment.complete(Lesson("Databases", 20))
except UnknownLessonError as err:
    print("refused:", err)

empty = Course("Coming Soon", 0, Level.BEGINNER)
print(empty.enrol(lukas).progress)

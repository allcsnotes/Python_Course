from domain import Course, Level, Student
from storage import load_courses, save_courses

course = Course("Python Basics", 499, Level.BEGINNER)
course.add_lesson("Variables", 12)
course.add_lesson("Loops", 15)
priya = Student("Priya", "priya@example.com")
enrollment = course.enrol(priya)
enrollment.complete(course.lessons[0])

save_courses([course], "courses.json")
print(open("courses.json").read())

loaded = load_courses("courses.json")[0]
print(loaded)
print(loaded.enrollments[priya.email].progress)

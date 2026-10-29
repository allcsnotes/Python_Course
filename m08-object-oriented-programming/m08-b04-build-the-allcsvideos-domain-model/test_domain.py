from domain import AlreadyEnrolledError, UnknownLessonError
from domain import Course, Lesson, Level, Student
from storage import load_courses, save_courses

results = []


def check(label, ok):
    results.append(ok)
    print("PASS" if ok else "FAIL", label)


def raises(error, action):
    try:
        action()
    except error:
        return True
    return False


def new_course(price):
    return Course("Python Basics", price, Level.BEGINNER)


course = new_course(499)
course.add_lesson("Variables", 12)
course.add_lesson("Loops", 15)
course.add_lesson("Functions", 18)
first, second, third = course.lessons
priya = Student("Priya", "priya@example.com")
enrollment = course.enrol(priya)

check("price 499 is accepted", course.price == 499)
check("negative price is refused",
      raises(ValueError, lambda: new_course(-1)))
check("price with paise is refused",
      raises(ValueError, lambda: new_course(499.5)))
check("lesson of 0 minutes is refused",
      raises(ValueError, lambda: Lesson("Empty", 0)))
check("email without @ is refused",
      raises(ValueError, lambda: Student("Lukas", "lukas")))
check("course counts its lessons", len(course) == 3)
check("enrolling twice is refused",
      raises(AlreadyEnrolledError,
             lambda: course.enrol(priya)))
check("progress starts at 0", enrollment.progress == 0)

enrollment.complete(first)
check("1 of 3 is 33 percent", enrollment.progress == 33)
enrollment.complete(first)
check("same lesson counts once", enrollment.progress == 33)
other = Lesson("Databases", 20)
check("lesson of another course is refused",
      raises(UnknownLessonError,
             lambda: enrollment.complete(other)))

enrollment.complete(second)
enrollment.complete(third)
check("3 of 3 lessons is finished", enrollment.finished)

save_courses([course], "test_courses.json")
again = load_courses("test_courses.json")[0]
saved = again.enrollments[priya.email]
check("save keeps the progress", saved.progress == 100)
check("save keeps the level", again.level is Level.BEGINNER)

passed = results.count(True)
print(passed, "of", len(results), "checks passed")

from domain import AlreadyEnrolledError
from domain import Course, Level, Student
from storage import load_courses, save_courses


def build_school():
    python = Course("Python Basics", 499, Level.BEGINNER)
    python.add_lesson("Variables", 12)
    python.add_lesson("Loops", 15)
    python.add_lesson("Functions", 18)
    sql = Course("SQL in a Weekend", 799, Level.INTERMEDIATE)
    sql.add_lesson("SELECT", 20)
    sql.add_lesson("JOIN", 25)
    return [python, sql]


def main():
    python, sql = build_school()
    print(python)
    print(len(python), "lessons,", python.minutes, "min")

    priya = Student("Priya", "priya@example.com")
    lukas = Student("Lukas", "lukas@example.com")
    first = python.enrol(priya)
    second = python.enrol(lukas)
    for lesson in python.lessons[:2]:
        first.complete(lesson)
    for lesson in python:
        second.complete(lesson)
    print("Priya:", first.progress, "percent")
    print("Lukas:", second.progress, "percent")

    try:
        python.enrol(priya)
    except AlreadyEnrolledError as err:
        print("Refused:", err)
    try:
        Course("Free Gift", -499, Level.BEGINNER)
    except ValueError as err:
        print("Refused:", err)

    save_courses([python, sql], "courses.json")
    loaded = load_courses("courses.json")
    print("Saved and loaded", len(loaded), "courses")
    saved = loaded[0].enrollments[priya.email]
    print("Priya is still at", saved.progress, "percent")


if __name__ == "__main__":
    main()

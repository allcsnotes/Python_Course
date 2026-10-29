courses = {"C101": "Python", "C102": "SQL"}


class UnknownCourseError(Exception):
    pass


def enrol(student, course_id):
    if course_id not in courses:
        raise UnknownCourseError(f"no course {course_id}")
    return (student, courses[course_id])


try:
    enrol("Lukas")
except UnknownCourseError as error:
    print("Sorry:", error)

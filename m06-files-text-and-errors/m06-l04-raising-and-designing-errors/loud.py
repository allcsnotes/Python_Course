courses = {"C101": "Python", "C102": "SQL"}


class UnknownCourseError(Exception):
    pass


def find_course(course_id):
    if course_id not in courses:
        raise UnknownCourseError(f"no course {course_id}")
    return courses[course_id]


title = find_course("C103")
print("Welcome to " + title.upper())

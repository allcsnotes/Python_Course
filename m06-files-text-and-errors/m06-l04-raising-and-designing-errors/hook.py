courses = {"C101": "Python", "C102": "SQL"}


def enrol(student, course_id):
    return (student, courses.get(course_id))


print(enrol("Lukas", "C103"))

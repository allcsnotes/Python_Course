courses = {"C101": "Python", "C102": "SQL"}


def find_course(course_id):
    return courses.get(course_id)


title = find_course("C103")
print("Welcome to " + title.upper())

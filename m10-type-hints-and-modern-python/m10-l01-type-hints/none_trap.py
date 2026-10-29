COURSES = {"C101": "Python Basics", "C102": "SQL Basics"}


def find_title(course_id: str) -> str | None:
    return COURSES.get(course_id)


print(find_title("C101").upper())
print(find_title("C999").upper())

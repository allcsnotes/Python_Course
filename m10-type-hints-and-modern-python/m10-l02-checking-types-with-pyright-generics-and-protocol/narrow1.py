COURSES = {"C101": "Python Basics", "C102": "SQL Basics"}


def find_title(course_id: str) -> str | None:
    return COURSES.get(course_id)


def show(course_id: str) -> None:
    title = find_title(course_id)
    print(title.upper())

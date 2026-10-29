COURSES = {"C101": "Python Basics", "C102": "SQL Basics"}


def find_title(course_id: str) -> str | None:
    return COURSES.get(course_id)


def show(course_id: str) -> None:
    title = find_title(course_id)
    reveal_type(title)
    if title is None:
        print("No such course")
        return
    reveal_type(title)
    print(title.upper())


show("C101")
show("C999")

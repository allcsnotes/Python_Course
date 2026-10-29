COURSES = [
    {"id": 1, "title": "Python", "price": 499, "level": "beginner"},
    {"id": 2, "title": "SQL", "price": 399, "level": "beginner"},
    {"id": 3, "title": "Docker", "price": 449, "level": "intermediate"},
]


def list_courses():
    return COURSES


print([course["title"] for course in list_courses()])

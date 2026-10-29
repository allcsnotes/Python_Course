import json

text = '{"title": "Python Basics", "price": 1499}'
course = json.loads(text)


def show(course):
    return f"{course['title']} costs {course['pirce']}"


print(show(course))

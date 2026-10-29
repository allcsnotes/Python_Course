from pydantic import ValidationError

from catalog import Course

data = {
    "title": "Python Basics",
    "instructor": {"name": "Meera", "email": "meera@example.com"},
    "lessons": [
        {"title": "Intro", "minutes": 12},
        {"title": "Setup", "minutes": "ten"},
    ],
}
try:
    Course(**data)
except ValidationError as err:
    for e in err.errors():
        print(".".join(str(p) for p in e["loc"]), "->", e["msg"])

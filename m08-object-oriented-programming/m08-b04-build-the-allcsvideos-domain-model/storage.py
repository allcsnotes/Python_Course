import json
from pathlib import Path

from domain import Course


def save_courses(courses, path):
    data = [course.to_dict() for course in courses]
    text = json.dumps(data, indent=2)
    Path(path).write_text(text, encoding="utf-8")


def load_courses(path):
    text = Path(path).read_text(encoding="utf-8")
    data = json.loads(text)
    return [Course.from_dict(item) for item in data]

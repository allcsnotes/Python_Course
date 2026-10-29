from sqlalchemy.orm import Session

from db import engine
from models import Course

COURSES = [
    ("SQL in Two Weeks", 399, "beginner"),
    ("Git and GitHub", 299, "beginner"),
    ("Docker for Developers", 599, "intermediate"),
    ("FastAPI in Practice", 699, "intermediate"),
    ("Async Python", 799, "advanced"),
    ("Python Performance", 899, "advanced"),
    ("Linux Essentials", 349, "beginner"),
]

with Session(engine) as session:
    session.add_all(
        Course(title=t, price=p, level=lv)
        for t, p, lv in COURSES
    )
    session.commit()

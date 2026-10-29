from sqlalchemy.orm import Session

from db import engine
from models import Course, Student

with Session(engine) as s, s.begin():
    s.add_all([
        Course(title="Python Basics", price=499, level="beginner"),
        Course(title="SQL in Docker", price=799, level="beginner"),
        Course(title="FastAPI Live Cohort", price=1499, level="advanced"),
        Student(name="Lukas"),
        Student(name="Priya"),
    ])
print("3 courses and 2 students saved")

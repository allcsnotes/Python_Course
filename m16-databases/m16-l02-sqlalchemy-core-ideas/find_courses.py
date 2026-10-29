from sqlalchemy import select
from sqlalchemy.orm import Session

from db import engine
from models import Course

stmt = (
    select(Course)
    .where(Course.price < 500)
    .order_by(Course.title)
)
print(stmt)

with Session(engine) as session:
    for course in session.scalars(stmt):
        print(course)

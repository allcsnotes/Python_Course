import os

os.environ["JWT_SECRET"] = "test-only-secret"
os.environ["DATABASE_URL"] = (
    "postgresql+psycopg://postgres:devpass@localhost:17403/allcs_test"
)

import pytest
from alembic import command
from alembic.config import Config
from fastapi.testclient import TestClient
from sqlalchemy import event
from sqlalchemy.orm import Session

from app.db import engine, get_session
from app.models import Course, Enrollment, Student
from app.main import app


@pytest.fixture(scope="session", autouse=True)
def schema():
    config = Config("alembic.ini")
    command.downgrade(config, "base")
    command.upgrade(config, "head")


@pytest.fixture
def session():
    connection = engine.connect()
    outer = connection.begin()
    session = Session(
        connection, join_transaction_mode="create_savepoint"
    )
    yield session
    session.close()
    outer.rollback()
    connection.close()


@pytest.fixture
def client(session):
    app.dependency_overrides[get_session] = lambda: session
    yield TestClient(app)
    app.dependency_overrides.clear()


class Counter:
    count = 0


@pytest.fixture
def queries():
    counter = Counter()

    def tick(*args):
        counter.count += 1

    event.listen(engine, "before_cursor_execute", tick)
    yield counter
    event.remove(engine, "before_cursor_execute", tick)


@pytest.fixture
def users(session):
    people = [
        ("lukas", "student"),
        ("priya", "student"),
        ("meera", "instructor"),
        ("asha", "admin"),
    ]
    made = {}
    for name, role in people:
        student = Student(
            name=name,
            email=f"{name}@example.com",
            role=role,
            password_hash="not-a-real-hash",
        )
        session.add(student)
        made[name] = student
    course = Course(title="Python Basics", price=499, level="beginner")
    session.add(course)
    session.flush()
    session.add(Enrollment(student_id=made["priya"].id, course_id=course.id))
    session.flush()
    return made


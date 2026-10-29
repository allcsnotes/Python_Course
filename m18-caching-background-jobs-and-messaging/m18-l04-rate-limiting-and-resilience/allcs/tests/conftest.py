import os

os.environ["DATABASE_URL"] = (
    "postgresql+psycopg://allcs:allcs@localhost:18504/allcs_test"
)
os.environ["REDIS_URL"] = "redis://localhost:18404/1"
os.environ["SECRET_KEY"] = "test-secret-not-for-production-1234"

import pytest
from alembic import command
from alembic.config import Config
from fastapi.testclient import TestClient
from sqlalchemy import event
from sqlalchemy.orm import Session

from app.cache import r
from app.db import engine, get_session
from app.main import app
from app.models import Student
from app.security import hash_password

PASSWORD = "demo-password-1"


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


@pytest.fixture(autouse=True)
def empty_redis():
    r.flushdb()


@pytest.fixture
def client(session):
    app.dependency_overrides[get_session] = lambda: session
    yield TestClient(app)
    app.dependency_overrides.clear()


@pytest.fixture
def make_user(session):
    def make(name, role="student", password=PASSWORD):
        student = Student(
            name=name,
            email=f"{name.lower().replace(' ', '')}@example.com",
            role=role,
            password_hash=password and hash_password(password),
        )
        session.add(student)
        session.flush()
        return student

    return make


@pytest.fixture
def login(client):
    def go(student, password=PASSWORD):
        form = {"username": student.email, "password": password}
        return client.post("/auth/login", data=form)

    return go


@pytest.fixture
def headers(login):
    def make(student):
        token = login(student).json()["access_token"]
        return {"Authorization": f"Bearer {token}"}

    return make


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

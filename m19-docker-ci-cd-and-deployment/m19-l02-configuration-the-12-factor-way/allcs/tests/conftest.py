import os

os.environ["DATABASE_URL"] = (
    "postgresql+psycopg://allcs:allcs@localhost:19502/allcs_test"
)
os.environ["SECRET_KEY"] = (
    "test-secret-not-for-production-1234"
)
os.environ["REDIS_URL"] = "redis://localhost:19402/15"

import pytest
from alembic import command
from alembic.config import Config
from app.worker import celery_app, redis
from fastapi.testclient import TestClient
from sqlalchemy import event
from sqlalchemy.orm import Session

from app import mailer
from app.db import engine, get_session
from app.main import app
from app.models import Student
from app.routers.auth import FAILED
from app.security import hash_password

PASSWORD = "demo-password-1"
celery_app.conf.task_always_eager = True


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
def forget_failed_logins():
    FAILED.clear()


@pytest.fixture(autouse=True)
def empty_redis():
    redis.flushdb()


class Mailbox:
    def __init__(self):
        self.sent = []
        self.failures = 0
        self.attempts = 0


@pytest.fixture(autouse=True)
def mailbox(monkeypatch):
    box = Mailbox()

    def fake_send(message):
        box.attempts += 1
        if box.failures > 0:
            box.failures -= 1
            raise ConnectionRefusedError(
                "mail server is down"
            )
        box.sent.append(message)

    monkeypatch.setattr(mailer, "send", fake_send)
    return box


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
            password_hash=password
            and hash_password(password),
        )
        session.add(student)
        session.flush()
        return student

    return make


@pytest.fixture
def login(client):
    def go(student, password=PASSWORD):
        form = {
            "username": student.email,
            "password": password,
        }
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

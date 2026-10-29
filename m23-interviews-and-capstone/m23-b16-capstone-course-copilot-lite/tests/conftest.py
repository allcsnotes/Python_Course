import os

TEST_DB = "postgresql+psycopg://copilot:copilot@localhost:23536/copilot_test"
os.environ["DATABASE_URL"] = os.environ.get(
    "TEST_DATABASE_URL", TEST_DB
)
os.environ["REDIS_URL"] = os.environ.get(
    "TEST_REDIS_URL", "redis://localhost:23436/15"
)
os.environ["SECRET_KEY"] = (
    "test-secret-key-not-for-production"
)

import pytest  # noqa: E402
from alembic import command  # noqa: E402
from alembic.config import Config  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402
from sqlalchemy import create_engine, text  # noqa: E402
from sqlalchemy.engine import make_url  # noqa: E402
from sqlalchemy.orm import Session  # noqa: E402

from app import mailer  # noqa: E402
from app.cache import redis  # noqa: E402
from app.db import engine  # noqa: E402
from app.main import app  # noqa: E402
from app.models import Lesson, User  # noqa: E402
from app.search import index_lesson  # noqa: E402
from app.security import hash_password, make_token  # noqa: E402
from app.worker import celery_app  # noqa: E402

celery_app.conf.task_always_eager = True
celery_app.conf.task_eager_propagates = True

FIND_DB = "select 1 from pg_database where datname = :n"


def create_test_database():
    url = make_url(os.environ["DATABASE_URL"])
    admin = create_engine(
        url.set(database="postgres"),
        isolation_level="AUTOCOMMIT",
    )
    with admin.connect() as conn:
        name = {"n": url.database}
        found = conn.scalar(text(FIND_DB), name)
        if not found:
            conn.execute(
                text(f'create database "{url.database}"')
            )


@pytest.fixture(scope="session", autouse=True)
def schema():
    create_test_database()
    config = Config("alembic.ini")
    command.downgrade(config, "base")
    command.upgrade(config, "head")


@pytest.fixture(autouse=True)
def clean():
    redis.flushdb()
    yield
    with engine.begin() as conn:
        conn.execute(
            text(
                "truncate users, lessons, notes, progress "
                "restart identity cascade"
            )
        )


@pytest.fixture
def mailbox(monkeypatch):
    sent = []
    monkeypatch.setattr(mailer, "send", sent.append)
    return sent


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def make_user():
    def make(name="Lukas", role="student"):
        with Session(engine) as session:
            user = User(
                email=f"{name.lower()}@example.com",
                name=name,
                role=role,
                password_hash=hash_password(
                    "a-long-password"
                ),
            )
            session.add(user)
            session.commit()
            return user.id, make_token(user.id, role)

    return make


@pytest.fixture
def auth(make_user):
    def headers(name="Lukas", role="student"):
        _, token = make_user(name, role)
        return {"Authorization": f"Bearer {token}"}

    return headers


@pytest.fixture
def add_lesson():
    def add(code, title, notes):
        with Session(engine) as session:
            lesson = Lesson(
                code=code, title=title, notes=notes
            )
            session.add(lesson)
            session.flush()
            index_lesson(session, lesson.id)
            session.commit()
            return lesson.id

    return add

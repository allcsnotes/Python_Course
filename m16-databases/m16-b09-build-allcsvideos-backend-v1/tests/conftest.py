import os

os.environ["DATABASE_URL"] = (
    "postgresql+psycopg://allcs:allcs@localhost:15409/allcs_test"
)

import pytest
from alembic import command
from alembic.config import Config
from fastapi.testclient import TestClient
from sqlalchemy import event
from sqlalchemy.orm import Session

from app.db import engine, get_session
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
def make_course(client):
    def make(title="Python Basics", level="beginner", price=499):
        body = {"title": title, "price": price, "level": level}
        return client.post("/courses", json=body).json()

    return make

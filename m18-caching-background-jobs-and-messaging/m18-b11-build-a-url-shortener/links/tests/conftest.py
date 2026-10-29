import os

os.environ["DATABASE_URL"] = (
    "postgresql+psycopg://allcs:allcs@localhost:18511/links_test"
)
os.environ["REDIS_URL"] = "redis://localhost:18411/1"

import pytest
from alembic import command
from alembic.config import Config
from fastapi.testclient import TestClient
from sqlalchemy import event, text

from app import cache, settings
from app.db import engine
from app.main import app


@pytest.fixture(scope="session", autouse=True)
def schema():
    config = Config("alembic.ini")
    command.downgrade(config, "base")
    command.upgrade(config, "head")


@pytest.fixture(autouse=True)
def clean():
    cache.r.flushdb()
    with engine.begin() as connection:
        connection.execute(text("DELETE FROM links"))


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def make(client):
    def make_link(
        url="https://allcsvideos.com/courses/git", **more
    ):
        reply = client.post(
            "/links", json={"url": url, **more}
        )
        assert reply.status_code == 201, reply.text
        return reply.json()["code"]

    return make_link


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
def limit(monkeypatch):
    monkeypatch.setattr(settings, "RATE_LIMIT", 3)

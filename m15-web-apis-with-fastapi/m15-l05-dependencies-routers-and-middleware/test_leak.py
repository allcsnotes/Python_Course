from fastapi.testclient import TestClient

from deps_app import app, get_store
from store import Store

client = TestClient(app)


def test_empty_store():
    app.dependency_overrides[get_store] = lambda: Store({})
    assert client.get("/courses").json() == []


def test_real_store_has_two():
    assert len(client.get("/courses").json()) == 2

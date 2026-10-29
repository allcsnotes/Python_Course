import pytest
from fastapi.testclient import TestClient

from deps_app import app, get_store
from store import Store


@pytest.fixture
def client():
    app.dependency_overrides[get_store] = lambda: Store()
    yield TestClient(app)
    app.dependency_overrides.clear()


def test_add_course(client):
    new = {"title": "Rust", "price": 999}
    response = client.post("/courses", json=new)
    assert response.status_code == 201


def test_list_courses(client):
    courses = client.get("/courses").json()
    assert len(courses) == 2


def test_empty_store(client):
    app.dependency_overrides[get_store] = lambda: Store({})
    assert client.get("/courses").json() == []

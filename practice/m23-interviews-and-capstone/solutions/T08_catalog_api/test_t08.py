import pytest
from fastapi.testclient import TestClient

from catalog import Store, app, get_store


@pytest.fixture
def client():
    store = Store()                                     # a fresh store for every test
    app.dependency_overrides[get_store] = lambda: store
    yield TestClient(app)
    app.dependency_overrides.clear()


def make(client, title="Python", price=499, **extra):
    return client.post("/courses", json={"title": title, "price": price, **extra})


def test_create_and_read(client):
    created = make(client)
    assert created.status_code == 201
    assert created.headers["location"] == "/courses/1"
    assert created.json() == {"id": 1, "title": "Python", "price": 499, "level": "beginner"}
    assert client.get("/courses/1").json()["title"] == "Python"


@pytest.mark.parametrize("body", [
    {"title": "Py", "price": 1},
    {"title": "Python", "price": -5},
    {"title": "Python", "price": "free"},
    {"title": "Python", "price": 5, "level": "expert"},
    {"price": 5},
])
def test_validation_gives_422(client, body):
    assert client.post("/courses", json=body).status_code == 422


def test_duplicate_title_is_409_case_insensitive(client):
    make(client, "Python")
    assert make(client, "PYTHON").status_code == 409


def test_missing_course_is_404(client):
    assert client.get("/courses/99").status_code == 404
    assert client.delete("/courses/99").status_code == 404
    assert client.patch("/courses/99", json={"price": 1}).status_code == 404


def test_pagination_and_search(client):
    for n in range(25):
        make(client, f"Course {n:02d}")
    page = client.get("/courses", params={"limit": 10, "offset": 20}).json()
    assert page["total"] == 25 and len(page["items"]) == 5 and page["items"][0]["id"] == 21
    assert client.get("/courses", params={"q": "course 07"}).json()["total"] == 1
    assert client.get("/courses", params={"limit": 0}).status_code == 422
    assert client.get("/courses", params={"limit": 51}).status_code == 422


def test_patch_changes_only_given_fields(client):
    make(client, "Python", 499)
    changed = client.patch("/courses/1", json={"price": 399}).json()
    assert changed == {"id": 1, "title": "Python", "price": 399, "level": "beginner"}


def test_patch_title_clash_and_own_title(client):
    make(client, "Python")
    make(client, "SQL")
    assert client.patch("/courses/2", json={"title": "python"}).status_code == 409
    assert client.patch("/courses/2", json={"title": "SQL"}).status_code == 200   # own title is fine


def test_delete(client):
    make(client)
    assert client.delete("/courses/1").status_code == 204
    assert client.get("/courses/1").status_code == 404

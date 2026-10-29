from fastapi.testclient import TestClient

from hook_app import app

client = TestClient(app)


def test_add_course():
    new = {"title": "Rust", "price": 999}
    response = client.post("/courses", json=new)
    assert response.status_code == 201


def test_list_courses():
    courses = client.get("/courses").json()
    assert len(courses) == 2

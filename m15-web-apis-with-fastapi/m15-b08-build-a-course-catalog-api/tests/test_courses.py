import pytest


def add(client, title, level="beginner"):
    body = {"title": title, "price": 499, "level": level}
    return client.post("/courses", json=body)


def test_create_returns_201_and_an_id(client, python_course):
    response = client.post("/courses", json=python_course)
    assert response.status_code == 201
    assert response.json() == {"id": 1, **python_course}


def test_read_one_course(client, python_course):
    client.post("/courses", json=python_course)
    response = client.get("/courses/1")
    assert response.status_code == 200
    assert response.json()["title"] == "Python Basics"


def test_missing_course_is_a_404(client):
    response = client.get("/courses/99")
    assert response.status_code == 404
    assert response.json()["error"]["code"] == "course_not_found"


def test_duplicate_title_is_a_409(client, python_course):
    client.post("/courses", json=python_course)
    response = client.post("/courses", json=python_course)
    assert response.status_code == 409


@pytest.mark.parametrize(
    "bad",
    [
        {"title": "Go", "price": 499, "level": "beginner"},
        {"title": "Python Basics", "price": 0, "level": "beginner"},
        {"title": "Python Basics", "price": 499, "level": "expert"},
    ],
)
def test_bad_input_is_a_422(client, bad):
    response = client.post("/courses", json=bad)
    assert response.status_code == 422
    assert response.json()["error"]["code"] == "invalid_input"


def test_update_replaces_the_course(client, python_course):
    client.post("/courses", json=python_course)
    new = {**python_course, "price": 599}
    response = client.put("/courses/1", json=new)
    assert response.json()["price"] == 599


def test_delete_then_gone(client, python_course):
    client.post("/courses", json=python_course)
    assert client.delete("/courses/1").status_code == 204
    assert client.get("/courses/1").status_code == 404


def test_filter_by_level(client):
    add(client, "Python Basics")
    add(client, "Async Python", level="advanced")
    response = client.get("/courses", params={"level": "advanced"})
    assert response.json()["total"] == 1


def test_pagination_pages_and_total(client):
    for n in range(5):
        add(client, f"Course number {n}")
    params = {"limit": 2, "offset": 2}
    page = client.get("/courses", params=params).json()
    assert [c["id"] for c in page["items"]] == [3, 4]
    assert page["total"] == 5


def test_limit_above_fifty_is_a_422(client):
    response = client.get("/courses", params={"limit": 51})
    assert response.status_code == 422

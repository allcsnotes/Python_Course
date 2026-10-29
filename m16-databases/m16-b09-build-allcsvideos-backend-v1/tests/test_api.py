import pytest


def test_create_course(client):
    body = {"title": "Python Basics", "price": 499}
    r = client.post("/courses", json=body)
    assert r.status_code == 201
    assert r.json()["id"] > 0
    assert r.json()["level"] == "beginner"


def test_duplicate_title_is_409(client, make_course):
    make_course()
    body = {"title": "Python Basics", "price": 100}
    r = client.post("/courses", json=body)
    assert r.status_code == 409
    assert r.json()["error"]["code"] == "duplicate_title"


def test_missing_course_is_404(client):
    r = client.get("/courses/999999")
    assert r.status_code == 404
    assert r.json()["error"]["code"] == "not_found"


@pytest.mark.parametrize(
    "body",
    [
        {"title": "Py", "price": 100},
        {"title": "Python Basics", "price": 0},
        {"title": "Python Basics", "price": 5, "level": "expert"},
    ],
)
def test_bad_bodies_are_422(client, body):
    r = client.post("/courses", json=body)
    assert r.status_code == 422
    assert r.json()["error"]["code"] == "invalid_input"


def test_lessons_come_with_the_course(client, make_course):
    course = make_course()
    url = f"/courses/{course['id']}/lessons"
    client.post(url, json={"title": "Welcome", "position": 1})
    client.post(url, json={"title": "Setup", "position": 2})
    r = client.get(f"/courses/{course['id']}")
    titles = [x["title"] for x in r.json()["lessons"]]
    assert titles == ["Welcome", "Setup"]


def test_filter_and_pages(client, make_course):
    for n in range(5):
        make_course(f"Beginner {n}")
    make_course("Expert Corner", level="advanced")
    r = client.get("/courses?level=beginner&limit=2&offset=2")
    page = r.json()
    assert [c["title"] for c in page["items"]] == [
        "Beginner 2",
        "Beginner 3",
    ]
    assert page["total"] == 5


def test_enroll_once_then_never_twice(client, make_course):
    course = make_course()
    student = client.post(
        "/students",
        json={"name": "Lukas", "email": "lukas@example.com"},
    ).json()
    url = f"/courses/{course['id']}/enrollments"
    first = client.post(url, json={"student_id": student["id"]})
    second = client.post(url, json={"student_id": student["id"]})
    assert first.status_code == 201
    assert second.status_code == 409
    assert second.json()["error"]["code"] == "already_enrolled"


def test_course_with_students_cannot_be_deleted(client, make_course):
    course = make_course()
    student = client.post(
        "/students",
        json={"name": "Meera", "email": "meera@example.com"},
    ).json()
    url = f"/courses/{course['id']}/enrollments"
    client.post(url, json={"student_id": student["id"]})
    r = client.delete(f"/courses/{course['id']}")
    assert r.status_code == 409
    assert r.json()["error"]["code"] == "course_has_students"


def test_student_sees_their_courses(client, make_course):
    a, b = make_course("Course A"), make_course("Course B")
    student = client.post(
        "/students",
        json={"name": "Priya", "email": "priya@example.com"},
    ).json()
    for course in (a, b):
        url = f"/courses/{course['id']}/enrollments"
        client.post(url, json={"student_id": student["id"]})
    r = client.get(f"/students/{student['id']}")
    titles = [c["title"] for c in r.json()["courses"]]
    assert titles == ["Course A", "Course B"]


def test_list_needs_few_queries(client, make_course, queries):
    for n in range(6):
        make_course(f"Course {n}")
    queries.count = 0
    client.get("/courses?limit=6")
    assert queries.count <= 3

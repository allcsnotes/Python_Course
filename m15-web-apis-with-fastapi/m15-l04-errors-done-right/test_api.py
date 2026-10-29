from fastapi.testclient import TestClient

from g_good import app

client = TestClient(
    app, raise_server_exceptions=False
)


def test_missing_course():
    response = client.get("/courses/99")
    assert response.status_code == 404
    error = response.json()["error"]
    assert error["code"] == "course_not_found"


def test_double_enrol():
    response = client.post("/enrol/Lukas/1")
    assert response.status_code == 409


def test_crash_hides_details():
    response = client.get("/courses/1/students")
    assert response.status_code == 500
    assert "db:5432" not in response.text

import pytest
from fastapi.testclient import TestClient

from app.deps import get_store
from app.main import app
from app.store import CourseStore


@pytest.fixture
def client():
    store = CourseStore()
    app.dependency_overrides[get_store] = lambda: store
    yield TestClient(app)
    app.dependency_overrides.clear()


@pytest.fixture
def python_course():
    return {"title": "Python Basics", "price": 499, "level": "beginner"}

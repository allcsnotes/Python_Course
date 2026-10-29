from fastapi.testclient import TestClient

from deps_more import app, require_key

client = TestClient(app)


def test_delete_needs_a_key():
    assert client.delete("/courses/1").status_code == 401


def test_delete_with_key_switched_off():
    app.dependency_overrides[require_key] = lambda: None
    assert client.delete("/courses/1").status_code == 204
    app.dependency_overrides.clear()

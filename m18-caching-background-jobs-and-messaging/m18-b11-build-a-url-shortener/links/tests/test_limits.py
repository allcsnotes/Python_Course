from fastapi.testclient import TestClient

from app.main import app

BODY = {"url": "https://allcsvideos.com/courses/git"}


def test_the_fourth_request_is_refused(client, limit):
    for _ in range(3):
        assert (
            client.post("/links", json=BODY).status_code
            == 201
        )
    reply = client.post("/links", json=BODY)
    assert reply.status_code == 429
    assert 1 <= int(reply.headers["retry-after"]) <= 61
    assert (
        reply.json()["error"]["code"] == "too_many_requests"
    )


def test_every_address_has_its_own_counter(limit):
    one = TestClient(app, client=("10.0.0.1", 5000))
    two = TestClient(app, client=("10.0.0.2", 5000))
    for _ in range(3):
        one.post("/links", json=BODY)
    assert one.post("/links", json=BODY).status_code == 429
    assert two.post("/links", json=BODY).status_code == 201


def test_redirects_are_not_limited(client, make, limit):
    code = make()
    for _ in range(10):
        reply = client.get("/" + code, follow_redirects=False)
        assert reply.status_code == 307

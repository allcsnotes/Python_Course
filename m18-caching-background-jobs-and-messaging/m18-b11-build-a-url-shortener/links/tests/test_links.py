import pytest
from sqlalchemy import text

from app import cache
from app.db import engine

PAST = (
    "UPDATE links SET expires_at = now() - interval '1 hour'"
)


def test_create_returns_a_short_link(client):
    reply = client.post(
        "/links",
        json={"url": "https://allcsvideos.com/courses/git"},
    )
    assert reply.status_code == 201
    body = reply.json()
    assert len(body["code"]) == 7
    assert body["short_url"].endswith("/" + body["code"])
    assert body["expires_at"] is None


@pytest.mark.parametrize(
    "url",
    [
        "javascript:alert(1)",
        "ftp://files.example.com/a",
        "allcsvideos.com/courses",
        "https://",
        "https://example.com/" + "a" * 2100,
    ],
    ids=[
        "javascript",
        "ftp",
        "no scheme",
        "no host",
        "too long",
    ],
)
def test_only_good_http_urls_are_accepted(client, url):
    reply = client.post("/links", json={"url": url})
    assert reply.status_code == 422
    assert reply.json()["error"]["code"] == "invalid_input"


def test_extra_fields_are_refused(client):
    body = {"url": "https://example.com", "code": "mine"}
    assert client.post("/links", json=body).status_code == 422


def test_redirect_is_307_with_location(client, make):
    code = make("https://allcsvideos.com/courses/git")
    reply = client.get("/" + code, follow_redirects=False)
    assert reply.status_code == 307
    assert reply.headers["location"] == (
        "https://allcsvideos.com/courses/git"
    )


def test_unknown_code_is_404(client):
    assert (
        client.get(
            "/nope1234", follow_redirects=False
        ).status_code
        == 404
    )


def test_odd_characters_are_refused(client):
    reply = client.get("/a-b_c", follow_redirects=False)
    assert reply.status_code == 422


def test_expired_link_is_410(client, make):
    code = make(expires_in_days=1)
    with engine.begin() as connection:
        connection.execute(text(PAST))
    cache.r.flushdb()
    reply = client.get("/" + code, follow_redirects=False)
    assert reply.status_code == 410


def test_a_taken_code_is_retried(client, make, monkeypatch):
    first = make()
    answers = iter([first, first, "freeCode"])
    monkeypatch.setattr(
        "app.links.new_code", lambda: next(answers)
    )
    second = make("https://allcsvideos.com/courses/python")
    assert second == "freeCode"

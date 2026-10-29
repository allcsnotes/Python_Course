"""Needs Postgres on 23604 and Redis on 23404 (containers m23p04-pg and m23p04-redis)."""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import event

import shortener
from shortener import Base, PREFIX, app, cache, engine


@pytest.fixture
def client():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    for key in cache.scan_iter(f"{PREFIX}*"):
        cache.delete(key)
    yield TestClient(app, follow_redirects=False)
    Base.metadata.drop_all(engine)
    for key in cache.scan_iter(f"{PREFIX}*"):
        cache.delete(key)


def make(client, url="https://allcsvideos.com/python", **extra):
    return client.post("/links", json={"url": url, **extra})


def test_create_and_redirect(client):
    created = make(client)
    assert created.status_code == 201
    code = created.json()["code"]
    assert len(code) == 7
    hop = client.get(f"/{code}")
    assert hop.status_code == 307 and hop.headers["location"] == "https://allcsvideos.com/python"


def test_unknown_code_and_bad_url(client):
    assert client.get("/nope").status_code == 404
    assert make(client, url="not a url").status_code == 422
    assert make(client, url="ftp://example.com/x").status_code == 422


def test_custom_code_and_conflict(client):
    assert make(client, code="python").json()["code"] == "python"
    assert make(client, url="https://example.com/other", code="python").status_code == 409
    assert make(client, code="a b").status_code == 422


def test_idempotency_key(client):
    headers = {"Idempotency-Key": "k-1"}
    first = client.post("/links", json={"url": "https://example.com/a"}, headers=headers)
    again = client.post("/links", json={"url": "https://example.com/a"}, headers=headers)
    assert (first.status_code, again.status_code) == (201, 200)
    assert first.json() == again.json()


def test_second_visit_comes_from_the_cache(client):
    code = make(client).json()["code"]
    queries = []

    def record(conn, cursor, statement, *rest):
        queries.append(statement)

    event.listen(engine, "before_cursor_execute", record)
    try:
        client.get(f"/{code}")            # miss: asks Postgres
        assert len(queries) == 1
        client.get(f"/{code}")            # hit: no new query
        assert len(queries) == 1
    finally:
        event.remove(engine, "before_cursor_execute", record)
    assert 0 < cache.ttl(f"{PREFIX}url:{code}") <= shortener.CACHE_SECONDS


def test_clicks_are_counted(client):
    code = make(client).json()["code"]
    for _ in range(3):
        client.get(f"/{code}")
    assert client.get(f"/links/{code}/stats").json() == {"code": code, "clicks": 3}


def test_delete_invalidates_the_cache(client):
    code = make(client).json()["code"]
    client.get(f"/{code}")                                  # now cached
    assert cache.exists(f"{PREFIX}url:{code}")
    assert client.delete(f"/links/{code}").status_code == 204
    assert not cache.exists(f"{PREFIX}url:{code}")
    assert client.get(f"/{code}").status_code == 404        # not served from a stale cache
    assert client.delete(f"/links/{code}").status_code == 404


def test_rate_limit(client):
    codes = [make(client, url=f"https://example.com/{i}").status_code for i in range(7)]
    assert codes == [201] * 5 + [429, 429]
    blocked = make(client)
    assert 1 <= int(blocked.headers["retry-after"]) <= 60
    other = client.post("/links", json={"url": "https://example.com/x"}, headers={"X-Api-Key": "lukas"})
    assert other.status_code == 201                          # a different caller has its own budget

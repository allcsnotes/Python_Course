from sqlalchemy import text

from app import cache
from app.db import engine

SOON = (
    "UPDATE links SET expires_at = "
    "now() + interval '1 minute'"
)


def test_second_redirect_does_not_ask_postgres(
    client, make, queries
):
    code = make()
    client.get("/" + code, follow_redirects=False)
    before = queries.count
    client.get("/" + code, follow_redirects=False)
    assert queries.count == before


def test_hits_and_misses_are_counted(client, make):
    code = make()
    for _ in range(4):
        client.get("/" + code, follow_redirects=False)
    assert client.get("/cache/stats").json() == {
        "hits": 3,
        "misses": 1,
    }


def test_a_cached_link_has_a_time_to_live(client, make):
    code = make()
    client.get("/" + code, follow_redirects=False)
    assert 0 < cache.r.ttl(cache.link_key(code)) <= 3600


def test_a_link_that_expires_soon_is_cached_for_less(
    client, make
):
    code = make(expires_in_days=1)
    with engine.begin() as connection:
        connection.execute(text(SOON))
    client.get("/" + code, follow_redirects=False)
    assert 0 < cache.r.ttl(cache.link_key(code)) <= 60

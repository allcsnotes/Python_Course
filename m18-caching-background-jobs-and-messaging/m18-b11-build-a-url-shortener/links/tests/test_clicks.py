from app import cache


def test_clicks_wait_in_redis_until_the_flush(client, make):
    code = make()
    for _ in range(3):
        client.get("/" + code, follow_redirects=False)
    stats = client.get(f"/links/{code}/stats").json()
    assert (stats["clicks"], stats["pending"]) == (0, 3)
    assert cache.flush_clicks() == 3
    stats = client.get(f"/links/{code}/stats").json()
    assert (stats["clicks"], stats["pending"]) == (3, 0)


def test_the_flush_adds_to_what_is_stored(client, make):
    code = make()
    client.get("/" + code, follow_redirects=False)
    cache.flush_clicks()
    client.get("/" + code, follow_redirects=False)
    client.get("/" + code, follow_redirects=False)
    cache.flush_clicks()
    assert (
        client.get(f"/links/{code}/stats").json()["clicks"]
        == 3
    )

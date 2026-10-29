from app import cache
from app.metrics import SEARCHES


def ask(client, headers, q):
    return client.get(
        "/search", params={"q": q}, headers=headers
    )


def test_search_needs_a_token(client):
    assert client.get("/search?q=cache").status_code == 401


def test_finds_the_best_lesson_first(
    client, auth, add_lesson
):
    add_lesson(
        "A", "Threads", "Threads wait for the network."
    )
    add_lesson(
        "B", "Caching", "A cache keeps the answer. Cache!"
    )
    body = ask(client, auth(), "cache answer").json()
    assert body["results"][0]["code"] == "B"
    assert (
        "[cache]" in body["results"][0]["snippet"].lower()
    )


def test_any_word_can_match_but_unknown_words_find_nothing(
    client, auth, add_lesson
):
    add_lesson(
        "A", "Threads", "Threads wait for the network."
    )
    headers = auth()
    assert (
        len(
            ask(client, headers, "network banana").json()[
                "results"
            ]
        )
        == 1
    )
    assert (
        ask(client, headers, "banana").json()["results"]
        == []
    )


def test_query_must_have_two_characters(client, auth):
    assert ask(client, auth(), "a").status_code == 422


def test_second_search_is_a_cache_hit(
    client, auth, add_lesson
):
    add_lesson("A", "Caching", "A cache keeps the answer.")
    headers = auth()
    first = ask(client, headers, "cache")
    second = ask(client, headers, "  CACHE ")
    assert first.headers["x-cache"] == "MISS"
    assert second.headers["x-cache"] == "HIT"
    assert (
        second.json()["results"] == first.json()["results"]
    )


def test_invalidate_makes_the_next_search_a_miss(
    client, auth, add_lesson
):
    add_lesson("A", "Caching", "A cache keeps the answer.")
    headers = auth()
    ask(client, headers, "cache")
    cache.invalidate()
    assert (
        ask(client, headers, "cache").headers["x-cache"]
        == "MISS"
    )


def test_search_counter_counts_misses(
    client, auth, add_lesson
):
    add_lesson("A", "Caching", "A cache keeps the answer.")
    before = SEARCHES.labels("miss")._value.get()
    ask(client, auth(), "cache")
    assert (
        SEARCHES.labels("miss")._value.get() == before + 1
    )


def test_the_twenty_first_search_is_429(
    client, auth, monkeypatch
):
    from app.settings import get_settings

    monkeypatch.setattr(get_settings(), "search_limit", 3)
    headers = auth()
    codes = [
        ask(client, headers, "cache").status_code
        for _ in range(4)
    ]
    assert codes == [200, 200, 200, 429]
    last = ask(client, headers, "cache")
    assert int(last.headers["retry-after"]) <= 60

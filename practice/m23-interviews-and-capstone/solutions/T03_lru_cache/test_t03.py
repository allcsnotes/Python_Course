import pytest

from lru import LRUCache


def test_basic_get_put():
    cache = LRUCache(2)
    cache.put("a", 1)
    assert cache.get("a") == 1
    assert cache.get("zzz") is None
    assert cache.get("zzz", 0) == 0


def test_evicts_least_recently_used():
    cache = LRUCache(2)
    cache.put("a", 1)
    cache.put("b", 2)
    cache.get("a")                  # a is now fresh, b is the oldest
    cache.put("c", 3)
    assert "b" not in cache and "a" in cache and "c" in cache
    assert cache.keys() == ["a", "c"]


def test_put_existing_key_updates_and_refreshes():
    cache = LRUCache(2)
    cache.put("a", 1)
    cache.put("b", 2)
    cache.put("a", 10)
    cache.put("c", 3)
    assert cache.get("a") == 10 and "b" not in cache
    assert len(cache) == 2


def test_hit_and_miss_counters():
    cache = LRUCache(1)
    cache.put("a", 1)
    cache.get("a"); cache.get("a"); cache.get("b")
    assert (cache.hits, cache.misses) == (2, 1)


def test_contains_does_not_refresh():
    cache = LRUCache(2)
    cache.put("a", 1); cache.put("b", 2)
    assert "a" in cache
    cache.put("c", 3)               # a was only looked at with `in`, so it goes
    assert "a" not in cache


def test_capacity_must_be_positive():
    with pytest.raises(ValueError):
        LRUCache(0)

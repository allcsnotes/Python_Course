import hashlib
import json
from typing import cast

from redis import Redis

from app.settings import get_settings

redis = Redis.from_url(
    str(get_settings().redis_url), decode_responses=True
)
GENERATION = "search:generation"


def key_for(query):
    clean = " ".join(query.lower().split())
    digest = hashlib.sha1(clean.encode()).hexdigest()[:12]
    generation = redis.get(GENERATION) or 0
    return f"search:{generation}:{digest}"


def get(query):
    raw = cast(str | None, redis.get(key_for(query)))
    return json.loads(raw) if raw else None


def put(query, results):
    seconds = get_settings().cache_seconds
    redis.set(
        key_for(query), json.dumps(results), ex=seconds
    )


def invalidate():
    return redis.incr(GENERATION)

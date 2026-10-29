import json
import os

import redis

r = redis.Redis(
    port=int(os.environ.get("REDIS_PORT", "23403")),
    socket_timeout=0.2,
    decode_responses=True,
)
TTL = 60


def cached(key, load):
    try:
        hit = r.get(key)
        if hit:
            return json.loads(hit), "hit"
    except redis.RedisError:
        return load(), "down"
    value = load()
    try:
        r.set(key, json.dumps(value), ex=TTL)
    except redis.RedisError:
        pass
    return value, "miss"


def forget(key):
    try:
        r.delete(key)
    except redis.RedisError:
        pass

import hashlib
import os

import redis

r = redis.Redis(
    port=int(os.environ.get("REDIS_PORT", "18401")),
    decode_responses=True,
)
TTL = int(os.environ.get("CACHE_TTL", "60"))
LIST = "courses:list:"


def list_key(level, limit, offset):
    return f"{LIST}{level or 'all'}:{limit}:{offset}"


def forget_course_lists():
    keys = list(r.scan_iter(LIST + "*"))
    if keys:
        r.delete(*keys)


def blocked_key(token):
    digest = hashlib.sha256(token.encode()).hexdigest()
    return "blocked:" + digest

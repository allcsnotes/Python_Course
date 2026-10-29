import logging

import redis
from fastapi import HTTPException

from app.cache import r

log = logging.getLogger("allcs.ratelimit")

LIMIT = 5
WINDOW = 60


def login_key(ip, email):
    return f"login:{ip}:{email.lower()}"


def check_login(key):
    try:
        used = int(r.get(key) or 0)
        if used >= LIMIT:
            wait = max(r.ttl(key), 1)
            raise HTTPException(
                429,
                "Too many login attempts",
                headers={"Retry-After": str(wait)},
            )
    except redis.RedisError:
        log.error("redis is down, login limit skipped")


def record_failure(key):
    try:
        pipe = r.pipeline()
        pipe.set(key, 0, ex=WINDOW, nx=True)
        pipe.incr(key)
        return pipe.execute()[1]
    except redis.RedisError:
        log.error("redis is down, failure not counted")
        return 0


def forget(key):
    try:
        r.delete(key)
    except redis.RedisError:
        pass

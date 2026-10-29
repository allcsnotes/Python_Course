import logging
import time

import redis
from fastapi import Request

from app import settings
from app.cache import r
from app.errors import fail

log = logging.getLogger(__name__)


def rate_limit(request: Request):
    ip = request.client.host
    now = time.time()
    window = int(now // settings.RATE_WINDOW)
    key = f"rate:{ip}:{window}"
    try:
        pipe = r.pipeline()
        pipe.incr(key)
        pipe.expire(key, settings.RATE_WINDOW)
        count = pipe.execute()[0]
    except redis.RedisError:
        log.warning("redis is down: rate limit not checked")
        return
    if count > settings.RATE_LIMIT:
        wait = (
            int((window + 1) * settings.RATE_WINDOW - now) + 1
        )
        fail(
            429,
            "Too many links, try again later",
            headers={"Retry-After": str(wait)},
        )

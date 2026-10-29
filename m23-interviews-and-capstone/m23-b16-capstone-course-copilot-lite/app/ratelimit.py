import time
from typing import cast

from fastapi import Depends, HTTPException

from app.cache import redis
from app.deps import current_user
from app.settings import get_settings

WINDOW = 60


def search_limit(user=Depends(current_user)):
    now = int(time.time())
    key = f"limit:search:{user.id}:{now // WINDOW}"
    count = cast(int, redis.incr(key))
    if count == 1:
        redis.expire(key, WINDOW)
    if count > get_settings().search_limit:
        wait = WINDOW - now % WINDOW
        raise HTTPException(
            429,
            "too many searches",
            headers={"Retry-After": str(wait)},
        )
    return user

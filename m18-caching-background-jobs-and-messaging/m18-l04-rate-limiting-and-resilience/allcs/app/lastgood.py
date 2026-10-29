import logging

import redis

from app.cache import r

log = logging.getLogger("allcs.lastgood")
KEEP = 3600


def save(key, text):
    try:
        r.set("lastgood:" + key, text, ex=KEEP)
    except redis.RedisError:
        log.error("could not save the last good copy")


def load(key):
    try:
        return r.get("lastgood:" + key)
    except redis.RedisError:
        return None

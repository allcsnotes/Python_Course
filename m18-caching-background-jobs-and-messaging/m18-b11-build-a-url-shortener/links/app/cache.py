import json
import logging
from datetime import datetime, timezone

import redis
from sqlalchemy import update
from sqlalchemy.orm import Session

from app import settings
from app.db import engine
from app.models import Link

log = logging.getLogger(__name__)
r = redis.Redis.from_url(
    settings.REDIS_URL,
    decode_responses=True,
    socket_timeout=0.5,
    socket_connect_timeout=0.5,
)


def link_key(code):
    return f"link:{code}"


def clicks_key(code):
    return f"clicks:{code}"


def pack(url, expires_at):
    when = expires_at.isoformat() if expires_at else None
    return {"url": url, "expires_at": when}


def get_cached(code):
    raw = None
    try:
        if settings.CACHE_ENABLED:
            raw = r.get(link_key(code))
        r.incr("cache:hits" if raw else "cache:misses")
    except redis.RedisError:
        log.warning("redis is down: reading from postgres")
    return json.loads(raw) if raw else None


def put_cached(code, url, expires_at):
    if not settings.CACHE_ENABLED:
        return
    seconds = settings.CACHE_SECONDS
    if expires_at is not None:
        left = expires_at - datetime.now(timezone.utc)
        seconds = min(seconds, int(left.total_seconds()))
    if seconds <= 0:
        return
    value = json.dumps(pack(url, expires_at))
    try:
        r.set(link_key(code), value, ex=seconds)
    except redis.RedisError:
        log.warning("redis is down: link not cached")


def count_click(code):
    try:
        r.incr(clicks_key(code))
    except redis.RedisError:
        log.warning("redis is down: click not counted")


def pending_clicks(code):
    try:
        return int(r.get(clicks_key(code)) or 0)
    except redis.RedisError:
        return 0


def flush_clicks():
    taken = {}
    try:
        for key in r.scan_iter("clicks:*"):
            count = int(r.getdel(key) or 0)
            if count:
                taken[key.split(":", 1)[1]] = count
    except redis.RedisError:
        log.warning("redis is down: clicks not flushed")
    if not taken:
        return 0
    try:
        with Session(engine) as session:
            for code, count in taken.items():
                session.execute(
                    update(Link)
                    .where(Link.code == code)
                    .values(clicks=Link.clicks + count)
                )
            session.commit()
    except Exception:
        for code, count in taken.items():
            r.incrby(clicks_key(code), count)
        raise
    total = sum(taken.values())
    log.info("flushed %s clicks", total)
    return total

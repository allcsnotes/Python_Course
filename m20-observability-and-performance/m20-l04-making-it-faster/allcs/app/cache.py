import redis

from app.settings import get_settings

URL = str(get_settings().redis_url)
r = redis.Redis.from_url(
    URL,
    decode_responses=True,
    socket_connect_timeout=0.5,
    socket_timeout=0.5,
)

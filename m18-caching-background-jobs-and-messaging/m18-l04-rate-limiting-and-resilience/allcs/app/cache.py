import os

import redis

URL = os.environ.get("REDIS_URL", "redis://localhost:18404/0")
r = redis.Redis.from_url(
    URL,
    decode_responses=True,
    socket_connect_timeout=0.5,
    socket_timeout=0.5,
)

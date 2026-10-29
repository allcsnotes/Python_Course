import os
import time
from functools import lru_cache

import redis
from fastapi import FastAPI

app = FastAPI()
r = redis.Redis(port=18401, decode_responses=True)


@lru_cache
def catalog():
    return ["Python Basics", "SQL in Two Weeks"]


@app.get("/count")
def count():
    time.sleep(0.2)
    catalog()
    return {
        "pid": os.getpid(),
        "local_hits": catalog.cache_info().hits,
        "shared": r.incr("calls"),
    }

# Q37 - Cache-aside and invalidation (Redis in Docker)
import json
import time

import redis

cache = redis.Redis(host="localhost", port=23404, db=7, decode_responses=True)
database = {1: {"title": "Python", "price": 499}}      # stands in for Postgres
reads = {"database": 0}


def read_from_database(course_id):
    reads["database"] += 1
    return database[course_id]


def get_course(course_id, ttl=60):
    key = f"q37:course:{course_id}"
    cached = cache.get(key)                         # 1. look in the cache
    if cached is not None:
        return json.loads(cached), "hit"
    course = read_from_database(course_id)          # 2. miss: ask the database
    cache.set(key, json.dumps(course), ex=ttl)      # 3. remember it, with an expiry
    return course, "miss"


def update_price(course_id, price):
    database[course_id]["price"] = price
    cache.delete(f"q37:course:{course_id}")         # invalidate, or readers see the old price


cache.delete("q37:course:1")
print(get_course(1))
print(get_course(1))
print("database reads so far:", reads["database"])

database[1]["price"] = 399                          # change the database but forget the cache...
print("stale:", get_course(1))                      # ...and readers get the old price
update_price(1, 399)                                # the right way
print("fresh:", get_course(1))

print(get_course(1, ttl=1)[1], end=" ")             # the TTL is the safety net
cache.expire("q37:course:1", 1)
time.sleep(1.2)
print(get_course(1)[1], "(after the 1 second expiry)")
cache.delete("q37:course:1")

import redis

r = redis.Redis(port=18401, decode_responses=True)
used = r.info("memory")["used_memory"]
r.config_set("maxmemory", used + 2_000_000)
r.config_set("maxmemory-policy", "noeviction")
value = "x" * 1000

try:
    for n in range(10_000):
        r.set(f"page:{n}", value)
except redis.ResponseError as err:
    print("stopped at", n, "->", err)

r.config_set("maxmemory-policy", "allkeys-lru")
for n in range(10_000):
    r.set(f"page:{n}", value)
print("keys kept:", r.dbsize(), "of 10000")
print("evicted:", r.info("stats")["evicted_keys"])
r.config_set("maxmemory", 0)

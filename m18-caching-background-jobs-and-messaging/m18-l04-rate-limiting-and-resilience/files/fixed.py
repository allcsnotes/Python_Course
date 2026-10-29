import time

import redis

r = redis.Redis(port=18404, decode_responses=True)
LIMIT, WINDOW = 5, 2


def allowed(user):
    window = int(time.time() // WINDOW)
    key = f"hits:{user}:{window}"
    count = r.incr(key)
    r.expire(key, WINDOW)
    return count <= LIMIT


# wait until 0.2 s before a window ends
time.sleep((WINDOW - 0.2 - time.time()) % WINDOW)
for n in range(1, 13):
    answer = "yes" if allowed("lukas") else "no"
    stamp = time.time() % WINDOW
    print(f"request {n:2}  at {stamp:.2f} s  {answer}")
    time.sleep(0.04)

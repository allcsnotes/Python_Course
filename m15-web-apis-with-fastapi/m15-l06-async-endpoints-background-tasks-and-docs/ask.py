import time

import httpx

start = time.perf_counter()
reply = httpx.get("http://localhost:8156/rating/forgot")
took = time.perf_counter() - start
print(reply.status_code, reply.json(), f"{took:.2f} seconds")

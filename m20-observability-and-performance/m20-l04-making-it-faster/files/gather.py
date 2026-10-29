import asyncio
import time

import httpx

BASE = "http://localhost:8204"
URLS = [f"/demo/rating/{i}" for i in range(1, 9)]


def one_by_one():
    with httpx.Client(base_url=BASE) as client:
        return [client.get(url) for url in URLS]


async def together():
    async with httpx.AsyncClient(base_url=BASE) as client:
        calls = [client.get(url) for url in URLS]
        return await asyncio.gather(*calls)


start = time.perf_counter()
one_by_one()
print(f"one by one: {time.perf_counter() - start:.2f} s")

start = time.perf_counter()
asyncio.run(together())
print(f"gather:     {time.perf_counter() - start:.2f} s")

import asyncio
import time

import httpx

URL = "http://localhost:8125/page/{}"


async def fetch(client, sem, n):
    async with sem:
        response = await client.get(URL.format(n))
    return response.status_code


async def main():
    sem = asyncio.Semaphore(10)
    start = time.perf_counter()
    async with httpx.AsyncClient() as client:
        jobs = [fetch(client, sem, n) for n in range(1, 101)]
        codes = await asyncio.gather(*jobs)
    print(codes.count(200), "ok,", codes.count(503), "busy")
    print(f"{time.perf_counter() - start:.1f} seconds")


asyncio.run(main())

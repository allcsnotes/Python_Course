import asyncio
import time

import httpx

URL = "http://localhost:8125/page/{}"


async def fetch(client, n):
    response = await client.get(URL.format(n))
    return response.json()["title"]


async def main():
    start = time.perf_counter()
    async with httpx.AsyncClient() as client:
        jobs = [fetch(client, n) for n in range(1, 21)]
        titles = await asyncio.gather(*jobs)
    seconds = time.perf_counter() - start
    print(titles[:3], "...")
    print(f"20 pages, async: {seconds:.1f} seconds")


asyncio.run(main())

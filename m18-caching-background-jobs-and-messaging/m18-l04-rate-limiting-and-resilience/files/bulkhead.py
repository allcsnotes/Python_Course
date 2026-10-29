import asyncio
import time

import httpx

URL = "http://localhost:8284/rate"
rates = asyncio.Semaphore(2)
start = time.perf_counter()


async def get_rate(client, n):
    async with rates:
        print(f"{time.perf_counter() - start:.1f} s call {n} starts")
        await client.get(URL)
        print(f"{time.perf_counter() - start:.1f} s call {n} done")


async def main():
    async with httpx.AsyncClient() as client:
        jobs = [get_rate(client, n) for n in range(1, 7)]
        await asyncio.gather(*jobs)


asyncio.run(main())

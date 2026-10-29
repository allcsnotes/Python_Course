import asyncio

import httpx

URL = "http://localhost:8125/page/{}"


async def fetch(client, n):
    response = await client.get(URL.format(n))
    return response.status_code


async def main():
    async with httpx.AsyncClient() as client:
        jobs = [fetch(client, n) for n in range(1, 101)]
        codes = await asyncio.gather(*jobs)
    print(codes.count(200), "ok,", codes.count(503), "busy")


asyncio.run(main())

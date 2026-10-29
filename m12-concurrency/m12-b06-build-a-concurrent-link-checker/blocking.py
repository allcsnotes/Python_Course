import asyncio
import time

import httpx

from core import LINKS, OPTIONS, from_error, from_response, report


async def check(limit, url):
    async with limit:
        start = time.perf_counter()
        try:
            response = httpx.get(url, **OPTIONS)
        except httpx.HTTPError as error:
            return from_error(url, error, start)
        return from_response(url, response, start)


async def main():
    limit = asyncio.Semaphore(8)
    jobs = [check(limit, url) for url in LINKS]
    return await asyncio.gather(*jobs)


began = time.perf_counter()
results = asyncio.run(main())
report(results, time.perf_counter() - began)

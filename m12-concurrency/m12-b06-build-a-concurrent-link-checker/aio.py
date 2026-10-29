import asyncio
import time

import httpx

from core import LINKS, OPTIONS, from_error, from_response, report


async def check(client, limit, url):
    async with limit:
        start = time.perf_counter()
        try:
            response = await client.get(url)
        except httpx.HTTPError as error:
            return from_error(url, error, start)
        return from_response(url, response, start)


async def run_async(links, workers):
    limit = asyncio.Semaphore(workers)
    async with httpx.AsyncClient(**OPTIONS) as client:
        jobs = [check(client, limit, url) for url in links]
        return await asyncio.gather(*jobs)


def run(links, workers=8):
    return asyncio.run(run_async(links, workers))


if __name__ == "__main__":
    began = time.perf_counter()
    results = run(LINKS)
    report(results, time.perf_counter() - began)

import asyncio
import time


async def fetch(page):
    await asyncio.sleep(1)
    return page


async def main():
    start = time.perf_counter()
    a = asyncio.create_task(fetch("python"))
    b = asyncio.create_task(fetch("pytest"))
    c = asyncio.create_task(fetch("git"))
    print(await a, await b, await c)
    print(f"took {time.perf_counter() - start:.2f} s")


asyncio.run(main())

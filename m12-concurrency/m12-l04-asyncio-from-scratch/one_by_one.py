import asyncio
import time


async def fetch(page):
    await asyncio.sleep(1)
    return page


async def main():
    start = time.perf_counter()
    a = await fetch("python")
    b = await fetch("pytest")
    c = await fetch("git")
    print(a, b, c)
    print(f"took {time.perf_counter() - start:.2f} s")


asyncio.run(main())

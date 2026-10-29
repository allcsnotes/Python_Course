import asyncio
import time


async def fetch(page):
    time.sleep(1)
    return page


async def main():
    start = time.perf_counter()
    pages = await asyncio.gather(
        fetch("python"), fetch("pytest"), fetch("git"))
    print(pages)
    print(f"took {time.perf_counter() - start:.2f} s")


asyncio.run(main())

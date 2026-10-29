import asyncio
import time


async def fetch(page):
    await asyncio.sleep(1)
    return page


async def main():
    start = time.perf_counter()
    async with asyncio.TaskGroup() as group:
        a = group.create_task(fetch("python"))
        b = group.create_task(fetch("pytest"))
        c = group.create_task(fetch("git"))
    print(a.result(), b.result(), c.result())
    print(f"took {time.perf_counter() - start:.2f} s")


asyncio.run(main())

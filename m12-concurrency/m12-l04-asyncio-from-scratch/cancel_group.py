import asyncio
import time


async def slow():
    try:
        await asyncio.sleep(5)
    finally:
        print("slow: stopped early")


async def broken():
    await asyncio.sleep(0.5)
    raise ValueError("boom")


async def main():
    start = time.perf_counter()
    try:
        async with asyncio.TaskGroup() as group:
            group.create_task(slow())
            group.create_task(broken())
    except* ValueError:
        print("caught the error")
    print(f"took {time.perf_counter() - start:.2f} s")


asyncio.run(main())

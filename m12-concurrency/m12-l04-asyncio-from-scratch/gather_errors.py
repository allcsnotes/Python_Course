import asyncio


async def job(n):
    await asyncio.sleep(n / 10)
    if n > 1:
        raise ValueError(f"bad {n}")
    return "ok"


async def main():
    try:
        await asyncio.gather(job(1), job(2), job(3))
    except ValueError as error:
        print("first error only:", error)
    results = await asyncio.gather(
        job(1), job(2), job(3), return_exceptions=True)
    print(results)


asyncio.run(main())

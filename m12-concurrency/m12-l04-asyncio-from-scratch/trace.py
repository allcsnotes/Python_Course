import asyncio


async def fetch(page, seconds):
    print("start", page)
    await asyncio.sleep(seconds)
    print("done ", page)
    return page


async def main():
    results = await asyncio.gather(
        fetch("python", 3),
        fetch("pytest", 1),
        fetch("git", 2),
    )
    print(results)


asyncio.run(main())

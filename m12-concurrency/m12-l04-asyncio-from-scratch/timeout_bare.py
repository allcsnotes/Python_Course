import asyncio


async def slow_page():
    await asyncio.sleep(5)
    return "page"


async def main():
    async with asyncio.timeout(1):
        await slow_page()


asyncio.run(main())

import asyncio


async def inner():
    print("inner")


async def main():
    asyncio.run(inner())


asyncio.run(main())

import asyncio


async def hello():
    print("hello from a coroutine")


asyncio.run(hello())

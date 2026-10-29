import asyncio


class Door:
    async def __aenter__(self):
        print("enter: opening the door")
        await asyncio.sleep(0.5)
        return "the key"

    async def __aexit__(self, exc_type, exc, tb):
        await asyncio.sleep(0.5)
        print("exit: closing the door")


async def main():
    async with Door() as key:
        print("inside the block, with", key)
    print("after the block")


asyncio.run(main())

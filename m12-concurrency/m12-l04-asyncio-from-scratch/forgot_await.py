import asyncio


async def get_name():
    await asyncio.sleep(0.1)
    return "python"


async def main():
    name = get_name()
    print(name.upper())


asyncio.run(main())

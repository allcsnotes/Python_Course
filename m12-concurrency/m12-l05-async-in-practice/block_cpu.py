import asyncio

from beat import heartbeat


def crunch():
    return sum(i * i for i in range(30_000_000))


async def blocker():
    await asyncio.sleep(1)
    crunch()


async def main():
    await asyncio.gather(heartbeat(), blocker())


asyncio.run(main())

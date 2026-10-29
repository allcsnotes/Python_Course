import asyncio
import time

from beat import heartbeat


async def blocker():
    await asyncio.sleep(1)
    time.sleep(2)


async def main():
    await asyncio.gather(heartbeat(), blocker())


asyncio.run(main())

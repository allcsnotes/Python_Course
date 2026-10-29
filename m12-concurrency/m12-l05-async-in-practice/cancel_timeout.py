import asyncio

import httpx

SLOW = "http://localhost:8125/slow"


async def download(client):
    try:
        await client.get(SLOW)
    finally:
        print("download: cleaning up")


async def main():
    async with httpx.AsyncClient() as client:
        try:
            async with asyncio.timeout(1):
                await download(client)
        except TimeoutError:
            print("main: too slow, gave up")


asyncio.run(main())

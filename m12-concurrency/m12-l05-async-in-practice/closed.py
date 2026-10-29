import asyncio

import httpx

URL = "http://localhost:8125/page/1"


async def main():
    async with httpx.AsyncClient() as client:
        pass
    await client.get(URL)


asyncio.run(main())

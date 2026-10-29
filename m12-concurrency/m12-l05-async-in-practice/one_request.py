import asyncio

import httpx

URL = "http://localhost:8125/page/{}"


async def main():
    async with httpx.AsyncClient() as client:
        response = await client.get(URL.format(1))
    print(response.status_code, response.json())


asyncio.run(main())

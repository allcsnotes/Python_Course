import asyncio

from fastapi import FastAPI

app = FastAPI()


@app.get("/rating/forgot")
async def rating_forgot():
    asyncio.sleep(1)  # pretend: ask a slow rating service
    return {"rating": 4.8}

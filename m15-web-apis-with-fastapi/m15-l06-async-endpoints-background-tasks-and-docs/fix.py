import asyncio
import time

from fastapi import FastAPI

app = FastAPI()


@app.get("/rating/plain")
def rating_plain():
    time.sleep(1)
    return {"rating": 4.8}


@app.get("/rating/await")
async def rating_await():
    await asyncio.sleep(1)
    return {"rating": 4.8}


@app.get("/rating/blocked")
async def rating_blocked():
    time.sleep(1)
    return {"rating": 4.8}


@app.get("/rating/thread")
async def rating_thread():
    await asyncio.to_thread(time.sleep, 1)
    return {"rating": 4.8}


@app.get("/health")
async def health():
    return {"status": "ok"}

import time
import asyncio
from fastapi import FastAPI

app = FastAPI()


@app.get("/sync-sleep")
def sync_sleep():                   # plain def: FastAPI runs it in a worker thread
    time.sleep(0.4)
    return {"ok": True}


@app.get("/async-blocking")
async def async_blocking():         # async def + a blocking call: freezes the loop
    time.sleep(0.4)
    return {"ok": True}


@app.get("/async-correct")
async def async_correct():          # async def + await: the loop stays free
    await asyncio.sleep(0.4)
    return {"ok": True}

import time

from fastapi import FastAPI

app = FastAPI()


@app.get("/rating/plain")
def rating_plain():
    time.sleep(1)  # pretend: ask a slow rating service
    return {"rating": 4.8}


@app.get("/rating/async")
async def rating_async():
    time.sleep(1)  # the same slow service
    return {"rating": 4.8}

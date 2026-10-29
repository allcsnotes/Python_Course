from fastapi import FastAPI

from app.routers import courses
from app.store import Store

app = FastAPI()
STORE = Store()


def get_store() -> Store:
    return STORE


app.include_router(courses.router)

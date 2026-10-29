from typing import Annotated

from fastapi import Depends, FastAPI
from fastapi.testclient import TestClient

from store import Store

app = FastAPI()
STORE = Store()


def get_store() -> Store:
    return STORE


@app.get("/courses")
def list_courses(store: Annotated[Store, Depends(get_store)]):
    return list(store.courses.values())


print(TestClient(app).get("/courses").status_code)

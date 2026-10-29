from fastapi import Depends, FastAPI

from store import Store

app = FastAPI()


def get_store() -> Store:
    return Store()


@app.get("/courses")
def list_courses(store: Store = Depends(get_store())):
    return list(store.courses.values())

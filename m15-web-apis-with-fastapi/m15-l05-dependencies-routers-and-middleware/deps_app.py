from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel

from store import Store

app = FastAPI()
STORE = Store()


class NewCourse(BaseModel):
    title: str
    price: int


def get_store() -> Store:
    return STORE


@app.get("/courses")
def list_courses(store: Store = Depends(get_store)):
    return list(store.courses.values())


@app.get("/courses/{course_id}")
def get_course(
    course_id: int, store: Store = Depends(get_store)
):
    if course_id not in store.courses:
        raise HTTPException(404, "Course not found")
    return store.courses[course_id]


@app.post("/courses", status_code=201)
def add_course(
    body: NewCourse, store: Store = Depends(get_store)
):
    return store.add(body.title, body.price)

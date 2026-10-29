from fastapi import FastAPI
from pydantic import BaseModel

from store import Store

app = FastAPI()
store = Store()


class NewCourse(BaseModel):
    title: str
    price: int


@app.get("/courses")
def list_courses():
    return list(store.courses.values())


@app.post("/courses", status_code=201)
def add_course(body: NewCourse):
    return store.add(body.title, body.price)

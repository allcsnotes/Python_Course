"""Task 8 - a course catalogue API (FastAPI + pydantic, in-memory store)."""
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Query, Response
from pydantic import BaseModel, Field


class CourseIn(BaseModel):
    title: str = Field(min_length=3, max_length=80)
    price: int = Field(ge=0, description="whole rupees")
    level: str = Field(default="beginner", pattern="^(beginner|intermediate|advanced)$")


class CoursePatch(BaseModel):
    title: str | None = Field(default=None, min_length=3, max_length=80)
    price: int | None = Field(default=None, ge=0)


class CourseOut(CourseIn):
    id: int


class Page(BaseModel):
    items: list[CourseOut]
    total: int
    limit: int
    offset: int


class Store:
    def __init__(self):
        self.rows: dict[int, CourseOut] = {}
        self.next_id = 1

    def title_taken(self, title: str, except_id: int | None = None) -> bool:
        return any(c.title.lower() == title.lower() and c.id != except_id
                   for c in self.rows.values())


_default_store = Store()


def get_store() -> Store:
    return _default_store


StoreDep = Annotated[Store, Depends(get_store)]
app = FastAPI(title="Catalogue")


@app.post("/courses", status_code=201, response_model=CourseOut)
def create(body: CourseIn, store: StoreDep, response: Response):
    if store.title_taken(body.title):
        raise HTTPException(409, "a course with this title already exists")
    course = CourseOut(id=store.next_id, **body.model_dump())
    store.rows[course.id] = course
    store.next_id += 1
    response.headers["Location"] = f"/courses/{course.id}"
    return course


@app.get("/courses", response_model=Page)
def list_courses(store: StoreDep,
                 q: str | None = None,
                 limit: Annotated[int, Query(ge=1, le=50)] = 10,
                 offset: Annotated[int, Query(ge=0)] = 0):
    rows = sorted(store.rows.values(), key=lambda c: c.id)
    if q:
        rows = [c for c in rows if q.lower() in c.title.lower()]
    return Page(items=rows[offset:offset + limit], total=len(rows), limit=limit, offset=offset)


def _get_or_404(store: Store, course_id: int) -> CourseOut:
    if course_id not in store.rows:
        raise HTTPException(404, "course not found")
    return store.rows[course_id]


@app.get("/courses/{course_id}", response_model=CourseOut)
def read(course_id: int, store: StoreDep):
    return _get_or_404(store, course_id)


@app.patch("/courses/{course_id}", response_model=CourseOut)
def patch(course_id: int, body: CoursePatch, store: StoreDep):
    course = _get_or_404(store, course_id)
    changes = body.model_dump(exclude_unset=True)
    if "title" in changes and store.title_taken(changes["title"], except_id=course_id):
        raise HTTPException(409, "a course with this title already exists")
    updated = course.model_copy(update=changes)
    store.rows[course_id] = updated
    return updated


@app.delete("/courses/{course_id}", status_code=204)
def delete(course_id: int, store: StoreDep):
    _get_or_404(store, course_id)
    del store.rows[course_id]

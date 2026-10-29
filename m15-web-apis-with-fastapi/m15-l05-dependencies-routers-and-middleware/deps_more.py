from fastapi import Depends, FastAPI, Header, HTTPException

from store import Store

app = FastAPI()
STORE = Store()


def get_store() -> Store:
    return STORE


def paging(limit: int = 10, offset: int = 0) -> dict:
    return {"limit": limit, "offset": offset}


def get_course_or_404(
    course_id: int, store: Store = Depends(get_store)
):
    if course_id not in store.courses:
        raise HTTPException(404, "Course not found")
    return store.courses[course_id]


def require_key(x_api_key: str | None = Header(default=None)):
    if x_api_key != "secret-key":
        raise HTTPException(401, "Bad API key")


@app.get("/courses")
def list_courses(
    page: dict = Depends(paging),
    store: Store = Depends(get_store),
):
    courses = list(store.courses.values())
    start = page["offset"]
    return courses[start : start + page["limit"]]


@app.get("/courses/{course_id}")
def get_course(course: dict = Depends(get_course_or_404)):
    return course


@app.delete(
    "/courses/{course_id}",
    status_code=204,
    dependencies=[Depends(require_key)],
)
def delete_course(
    course: dict = Depends(get_course_or_404),
    store: Store = Depends(get_store),
):
    del store.courses[course["id"]]

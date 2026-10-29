from fastapi import FastAPI, HTTPException

from store import courses

app = FastAPI()


@app.get("/courses/{course_id}")
def get_course(course_id: int):
    if course_id not in courses:
        return HTTPException(404, "Not found")
    return courses[course_id]

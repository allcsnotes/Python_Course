from fastapi import FastAPI, HTTPException

from store import courses

app = FastAPI()


@app.get("/courses/{course_id}")
def get_course(course_id: int):
    course = courses.get(course_id)
    if course is None:
        raise HTTPException(
            status_code=404,
            detail=f"Course {course_id} not found",
        )
    return course

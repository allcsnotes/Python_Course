from fastapi import FastAPI

app = FastAPI()

courses = {
    1: {"id": 1, "title": "Python", "price": 499},
    2: {"id": 2, "title": "SQL", "price": 399},
}


@app.get("/courses/{course_id}")
def get_course(course_id: int):
    return courses.get(course_id)

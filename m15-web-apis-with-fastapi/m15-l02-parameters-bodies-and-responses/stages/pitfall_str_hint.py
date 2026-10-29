from fastapi import FastAPI, HTTPException

app = FastAPI()

COURSES = [
    {"id": 1, "title": "Python", "price": 499, "level": "beginner"},
    {"id": 2, "title": "SQL", "price": 399, "level": "beginner"},
    {"id": 3, "title": "Docker", "price": 449, "level": "intermediate"},
]


@app.get("/")
def home():
    return {"message": "Welcome to allcsvideos"}


@app.get("/courses")
def list_courses():
    return COURSES


@app.get("/courses/{course_id}")
def get_course(course_id: str):
    for course in COURSES:
        if course["id"] == course_id:
            return course
    raise HTTPException(
        status_code=404,
        detail="Course not found",
    )

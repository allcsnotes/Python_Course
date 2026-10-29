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
def list_courses(
    level: str | None = None,
    max_price: int | None = None,
    limit: int = 10,
):
    result = COURSES
    if level is not None:
        result = [c for c in result if c["level"] == level]
    if max_price is not None:
        result = [c for c in result if c["price"] <= max_price]
    return result[:limit]


@app.get("/courses/{course_id}")
def get_course(course_id: int):
    for course in COURSES:
        if course["id"] == course_id:
            return course
    raise HTTPException(
        status_code=404,
        detail="Course not found",
    )


@app.post("/courses")
def create_course(course: dict):
    course["id"] = max(c["id"] for c in COURSES) + 1
    COURSES.append(course)
    return course

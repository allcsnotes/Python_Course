from fastapi import FastAPI, HTTPException

app = FastAPI()

COURSES = [
    {
        "id": 1,
        "title": "Python",
        "price": 499,
        "level": "beginner",
        "cost": 120,
    },
    {
        "id": 2,
        "title": "SQL",
        "price": 399,
        "level": "beginner",
        "cost": 90,
    },
    {
        "id": 3,
        "title": "Docker",
        "price": 449,
        "level": "intermediate",
        "cost": 150,
    },
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


def find_index(course_id: int) -> int:
    for index, course in enumerate(COURSES):
        if course["id"] == course_id:
            return index
    raise HTTPException(
        status_code=404,
        detail="Course not found",
    )


@app.get("/courses/{course_id}")
def get_course(course_id: int):
    return COURSES[find_index(course_id)]


@app.post("/courses", status_code=201)
def create_course(course: dict):
    course["id"] = max(c["id"] for c in COURSES) + 1
    COURSES.append(course)
    return course


@app.put("/courses/{course_id}")
def replace_course(course_id: int, course: dict):
    index = find_index(course_id)
    course["id"] = course_id
    COURSES[index] = course
    return course


@app.delete("/courses/{course_id}", status_code=204)
def delete_course(course_id: int):
    del COURSES[find_index(course_id)]

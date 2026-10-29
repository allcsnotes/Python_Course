from api import app
from store import courses


@app.get("/courses")
def list_courses(limit: int = 10):
    return list(courses.values())[:limit]

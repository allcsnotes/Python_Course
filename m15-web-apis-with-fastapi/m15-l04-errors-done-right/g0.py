from api import app
import db


@app.get("/courses/{course_id}/students")
def students(course_id: int):
    db.connect()
    return []

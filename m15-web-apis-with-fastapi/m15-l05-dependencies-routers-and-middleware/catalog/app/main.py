from fastapi import FastAPI

from app.routers import courses, students

app = FastAPI(title="allcsvideos catalog")
app.include_router(courses.router)
app.include_router(students.router)


@app.get("/health")
def health():
    return {"status": "ok"}

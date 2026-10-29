from fastapi import FastAPI

app = FastAPI()
courses = []


@app.post("/courses", status_code=201)
def add_course(body: dict):
    courses.append(body)
    return body


@app.get("/total")
def total():
    return {"total": sum(c["price"] for c in courses)}

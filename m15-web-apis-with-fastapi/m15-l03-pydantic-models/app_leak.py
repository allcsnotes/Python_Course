from fastapi import FastAPI

from students import StudentIn

app = FastAPI()


@app.post("/students", status_code=201)
def join(student: StudentIn):
    return student

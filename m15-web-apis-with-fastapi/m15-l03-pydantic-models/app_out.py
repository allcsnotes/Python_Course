from fastapi import FastAPI

from students import StudentIn, StudentOut

app = FastAPI()


@app.post("/students", status_code=201, response_model=StudentOut)
def join(student: StudentIn):
    return {"id": 1, **student.model_dump()}

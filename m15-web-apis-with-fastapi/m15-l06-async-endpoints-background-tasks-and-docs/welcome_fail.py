from fastapi import BackgroundTasks, FastAPI
from pydantic import BaseModel

app = FastAPI()


class Enrolment(BaseModel):
    email: str
    course_id: int


def send_welcome_email(email: str, course_id: int):
    raise ConnectionError("the email service is down")


@app.post("/enrolments", status_code=201)
def enrol(
    enrolment: Enrolment, background_tasks: BackgroundTasks
):
    background_tasks.add_task(
        send_welcome_email,
        enrolment.email,
        enrolment.course_id,
    )
    return {"status": "enrolled"}

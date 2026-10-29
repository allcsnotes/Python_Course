import time

from fastapi import BackgroundTasks, FastAPI
from pydantic import BaseModel

app = FastAPI()


class Enrolment(BaseModel):
    email: str
    course_id: int


def send_welcome_email(email: str, course_id: int):
    time.sleep(2)  # pretend: talk to the email service
    print(f"email sent to {email} for course {course_id}")


@app.post("/enrolments/slow", status_code=201)
def enrol_slow(enrolment: Enrolment):
    send_welcome_email(enrolment.email, enrolment.course_id)
    return {"status": "enrolled"}


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

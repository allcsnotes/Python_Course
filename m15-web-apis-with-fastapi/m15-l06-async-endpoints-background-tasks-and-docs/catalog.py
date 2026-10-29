from fastapi import BackgroundTasks, FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(
    title="allcsvideos catalog API",
    description="Courses and enrolments for allcsvideos.com.",
    version="1.0.0",
)


class Course(BaseModel):
    id: int
    title: str = Field(examples=["Python Basics"])
    price: int = Field(description="In rupees", examples=[999])
    level: str


class Enrolment(BaseModel):
    email: str
    course_id: int


COURSES = {
    7: Course(
        id=7,
        title="Python from Zero to Production",
        price=1299,
        level="beginner",
    ),
}


def send_welcome_email(email: str, course_id: int):
    print(f"email sent to {email} for course {course_id}")


@app.get(
    "/courses/{course_id}",
    response_model=Course,
    responses={404: {"description": "No such course"}},
    tags=["courses"],
    summary="Get one course",
)
def get_course(course_id: int):
    """Return one course, or 404 if there is none."""
    if course_id not in COURSES:
        raise HTTPException(
            status_code=404, detail="Course not found"
        )
    return COURSES[course_id]


@app.post(
    "/enrolments",
    status_code=201,
    tags=["enrolments"],
    summary="Enrol a student",
)
def enrol(
    enrolment: Enrolment, background_tasks: BackgroundTasks
):
    """Save the enrolment now. The email goes out after."""
    background_tasks.add_task(
        send_welcome_email,
        enrolment.email,
        enrolment.course_id,
    )
    return {"status": "enrolled"}



@celery_app.task
def export_enrollments():
    import csv
    import io

    from sqlalchemy import select
    from sqlalchemy.orm import Session

    from app.db import engine
    from app.models import Course, Enrollment, Student

    query = (
        select(Student.name, Student.email, Course.title, Enrollment.enrolled_on)
        .join(Enrollment, Enrollment.student_id == Student.id)
        .join(Course, Course.id == Enrollment.course_id)
    )
    out = io.StringIO()
    writer = csv.writer(out)
    with Session(engine) as session:
        for row in session.execute(query):
            writer.writerow(row)
    logger.info("export done: %s rows", out.getvalue().count("\n"))

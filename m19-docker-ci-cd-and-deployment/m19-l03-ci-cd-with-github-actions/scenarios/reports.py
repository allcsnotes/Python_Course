from collections import Counter

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Course, Enrollment


def enrollments_per_course(session: Session):
    rows = session.execute(
        select(Enrollment.course_id)
    ).scalars()
    return Counter(rows)


def busiest_course(session: Session):
    counts = enrollments_per_course(session)
    if not counts:
        return None
    course_id, total = counts.most_common(1)[0]
    course = session.get(Course, course_id)
    if course is None:
        return None
    return {"title": course.title, "students": total}


def quiet_courses(session: Session, limit: int = 3):
    counts = enrollments_per_course(session)
    courses = session.scalars(select(Course)).all()
    ranked = sorted(
        courses, key=lambda c: counts.get(c.id, 0)
    )
    quiet = []
    for course in ranked:
        if counts.get(course.id, 0) == 0:
            quiet.append(course.title)
        if len(quiet) == limit:
            break
    return quiet


def report_lines(session: Session):
    lines = []
    counts = enrollments_per_course(session)
    for course in session.scalars(select(Course)):
        total = counts.get(course.id, 0)
        if total == 0:
            lines.append(f"{course.title}: nobody yet")
        elif total == 1:
            lines.append(f"{course.title}: one student")
        else:
            lines.append(
                f"{course.title}: {total} students"
            )
    busiest = busiest_course(session)
    if busiest:
        lines.append(f"busiest: {busiest['title']}")
    for title in quiet_courses(session):
        lines.append(f"needs a push: {title}")
    return lines


def report_text(session: Session):
    lines = report_lines(session)
    if not lines:
        return "no courses"
    return "\n".join(lines)

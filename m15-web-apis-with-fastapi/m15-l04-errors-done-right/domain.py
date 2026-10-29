from store import courses

enrolled = {("Lukas", 1)}


class CourseNotFound(Exception):
    pass


class AlreadyEnrolled(Exception):
    pass


def find_course(course_id):
    if course_id not in courses:
        raise CourseNotFound(course_id)
    return courses[course_id]


def enrol(student, course_id):
    find_course(course_id)
    if (student, course_id) in enrolled:
        raise AlreadyEnrolled(student)
    enrolled.add((student, course_id))
    return {"student": student, "course": course_id}

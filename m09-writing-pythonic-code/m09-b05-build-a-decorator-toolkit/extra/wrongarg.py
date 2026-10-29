from toolkit import require_login


@require_login
def enrol(user, course_id):
    return f"{user.name} is in {course_id}"


print(enrol("Lukas", "C101"))

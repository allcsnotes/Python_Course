from dataclasses import dataclass


@dataclass
class User:
    name: str
    logged_in: bool = False


def enrol(user, course_id):
    if not user.logged_in:
        return f"{user.name} must log in first"
    return f"{user.name} joined {course_id}"


print(enrol(User("Priya", True), "C101"))
print(enrol("Lukas", "C101"))

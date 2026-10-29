from dataclasses import dataclass


@dataclass
class User:
    name: str
    logged_in: bool = False


def enrol(user: User, course_id: str) -> str:
    if not user.logged_in:
        return f"{user.name} must log in first"
    return f"{user.name} joined {course_id}"


print(enrol(User("Priya", True), "C101"))
print(enrol(User("Lukas"), "C101"))

from dataclasses import dataclass

from toolkit import LoginRequiredError, require_login


@dataclass
class User:
    name: str
    logged_in: bool = False


@require_login
def enrol(user, course):
    return f"{user.name} is now in {course}"


priya = User("Priya", logged_in=True)
lukas = User("Lukas")

print(enrol(priya, "Python Basics"))
try:
    print(enrol(lukas, "Python Basics"))
except LoginRequiredError as error:
    print("refused:", error)

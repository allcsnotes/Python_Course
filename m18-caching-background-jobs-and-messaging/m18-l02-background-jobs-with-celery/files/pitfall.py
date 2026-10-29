from dataclasses import dataclass

from tasks import send_welcome_email


@dataclass
class Student:
    name: str
    email: str


lukas = Student("Lukas", "lukas@example.com")
send_welcome_email.delay(lukas, "Python Basics")

from dataclasses import dataclass


@dataclass
class Enrolled:
    student: str
    course: str


@dataclass
class Paid:
    student: str
    amount: int


def handle(event):
    match event:
        case Enrolled(student=who):
            return f"{who} joined"
        case Paid(who, amount):
            return f"{who} paid {amount}"
        case _:
            return "unknown"


print(handle(Enrolled("Lukas", "C101")))
print(handle(Paid("Priya", 1499)))
print(handle("Priya"))

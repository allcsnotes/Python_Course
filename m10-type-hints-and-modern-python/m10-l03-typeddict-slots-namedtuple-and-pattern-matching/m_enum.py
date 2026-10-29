from enum import Enum


class Plan(Enum):
    FREE = "free"
    PRO = "pro"


def label(plan):
    match plan:
        case Plan.FREE:
            return "no payment"
        case Plan.PRO:
            return "paid plan"
        case _:
            return "unknown"


print(label(Plan.PRO))
print(label(Plan.FREE))
print(label("pro"))

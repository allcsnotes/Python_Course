from typing import NamedTuple, NotRequired, TypedDict


class Event(TypedDict):
    type: str
    amount: NotRequired[int]


class Report(NamedTuple):
    income: int
    refunds: int


def summarise(events: list[Event]) -> Report:
    income = refunds = 0
    for event in events:
        match event:
            case {"type": "paid", "amount": rs} if rs > 0:
                income += rs
            case {"type": "refund", "amount": rs}:
                refunds += rs
    return Report(income, refunds)


events: list[Event] = [
    {"type": "paid", "amount": 1499},
    {"type": "login"},
    {"type": "paid", "amount": 999},
    {"type": "refund", "amount": 499},
]
report = summarise(events)
print(report)
income, refunds = report
print(income - refunds)

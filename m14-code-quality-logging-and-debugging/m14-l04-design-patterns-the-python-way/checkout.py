from typing import Protocol


class Gateway(Protocol):
    def charge(self, student: str, amount: int) -> str: ...


def checkout(student: str, price: int, gateway: Gateway) -> str:
    return gateway.charge(student, price)

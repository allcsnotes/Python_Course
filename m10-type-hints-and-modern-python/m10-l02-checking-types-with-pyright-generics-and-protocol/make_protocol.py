from typing import Protocol


class Payable(Protocol):
    def amount(self) -> int: ...


item = Payable()

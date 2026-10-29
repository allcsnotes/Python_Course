"""Task 6 - a cart with discount rules (OOP: dataclass, ABC, composition).

All money is whole rupees (int). GST is 18 percent of the discounted total.
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass, field

GST_PERCENT = 18


@dataclass(frozen=True)
class Item:
    name: str
    price: int
    qty: int = 1

    def __post_init__(self):
        if self.price < 0 or self.qty < 1:
            raise ValueError("price must be >= 0 and qty >= 1")

    @property
    def total(self) -> int:
        return self.price * self.qty


class Rule(ABC):
    label: str

    @abstractmethod
    def discount(self, items: list[Item], subtotal: int) -> int:
        """Rupees off. Must be 0 when the rule does not apply."""


@dataclass(frozen=True)
class PercentOff(Rule):
    percent: int
    min_subtotal: int = 0

    @property
    def label(self):
        return f"{self.percent}% off"

    def discount(self, items, subtotal):
        return subtotal * self.percent // 100 if subtotal >= self.min_subtotal else 0


@dataclass(frozen=True)
class FlatOff(Rule):
    amount: int
    min_subtotal: int = 0

    @property
    def label(self):
        return f"Rs {self.amount} off"

    def discount(self, items, subtotal):
        return self.amount if subtotal >= self.min_subtotal else 0


@dataclass(frozen=True)
class BundleFree(Rule):
    """Buy `needed` different items, and the cheapest one is free."""
    needed: int = 3
    label: str = "cheapest of the bundle free"

    def discount(self, items, subtotal):
        if len(items) < self.needed:
            return 0
        return min(item.price for item in items)


@dataclass
class Cart:
    items: list[Item] = field(default_factory=list)
    rules: list[Rule] = field(default_factory=list)

    def add(self, item: Item) -> None:
        for index, existing in enumerate(self.items):
            if existing.name == item.name:          # same course twice: add the quantities
                self.items[index] = Item(item.name, existing.price, existing.qty + item.qty)
                return
        self.items.append(item)

    @property
    def subtotal(self) -> int:
        return sum(item.total for item in self.items)

    def discounts(self) -> list[tuple[str, int]]:
        """Each rule is applied to the subtotal; the sum never exceeds the subtotal."""
        left = self.subtotal
        applied = []
        for rule in self.rules:
            amount = min(rule.discount(self.items, self.subtotal), left)
            if amount > 0:
                applied.append((rule.label, amount))
                left -= amount
        return applied

    def summary(self) -> dict:
        discount = sum(amount for _, amount in self.discounts())
        net = self.subtotal - discount
        gst = net * GST_PERCENT // 100
        return {"subtotal": self.subtotal, "discount": discount, "net": net,
                "gst": gst, "total": net + gst}

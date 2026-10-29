from dataclasses import dataclass

MAX_QUANTITY = 10


class CartError(Exception):
    """Base class for every problem the cart reports."""


class InvalidQuantity(CartError):
    pass


class InvalidPrice(CartError):
    pass


class UnknownItem(CartError):
    pass


@dataclass(frozen=True)
class Coupon:
    kind: str  # "percent" or "flat"
    value: int
    minimum: int = 0


COUPONS = {
    "SAVE10": Coupon("percent", 10),
}


class Cart:
    def __init__(self) -> None:
        self.items: dict[str, tuple[int, int]] = {}
        self.coupon: Coupon | None = None

    def add(self, name: str, price: int, quantity: int = 1) -> None:
        if not isinstance(price, int) or price <= 0:
            raise InvalidPrice(f"bad price {price!r}")
        have = self.items[name][1] if name in self.items else 0
        if quantity < 1:
            raise InvalidQuantity("quantity must be at least 1")
        if have + quantity > MAX_QUANTITY:
            raise InvalidQuantity(
                f"at most {MAX_QUANTITY} of one item"
            )
        self.items[name] = (price, have + quantity)

    def remove(self, name: str) -> None:
        if name not in self.items:
            raise UnknownItem(f"{name} is not in the cart")
        del self.items[name]

    def subtotal(self) -> int:
        return sum(p * q for p, q in self.items.values())

    def apply_coupon(self, code: str) -> None:
        self.coupon = COUPONS[code]

    def discount(self) -> int:
        if self.coupon is None:
            return 0
        return self.subtotal() * self.coupon.value // 100

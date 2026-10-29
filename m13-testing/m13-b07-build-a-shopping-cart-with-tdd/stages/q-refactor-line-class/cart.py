from dataclasses import dataclass

GST_PERCENT = 18
MAX_QUANTITY = 10


class CartError(Exception):
    """Base class for every problem the cart reports."""


class InvalidQuantity(CartError):
    pass


class InvalidPrice(CartError):
    pass


class UnknownItem(CartError):
    pass


class InvalidCoupon(CartError):
    pass


@dataclass(frozen=True)
class Coupon:
    kind: str  # "percent" or "flat"
    value: int
    minimum: int = 0


COUPONS = {
    "SAVE10": Coupon("percent", 10),
    "FLAT200": Coupon("flat", 200, minimum=1000),
    "WELCOME500": Coupon("flat", 500),
}


@dataclass
class Line:
    price: int
    quantity: int


class Cart:
    def __init__(self) -> None:
        self.items: dict[str, Line] = {}
        self.coupon: Coupon | None = None

    def add(self, name: str, price: int, quantity: int = 1) -> None:
        if not isinstance(price, int) or price <= 0:
            raise InvalidPrice(f"bad price {price!r}")
        have = self.items[name].quantity if name in self.items else 0
        if quantity < 1:
            raise InvalidQuantity("quantity must be at least 1")
        if have + quantity > MAX_QUANTITY:
            raise InvalidQuantity(
                f"at most {MAX_QUANTITY} of one item"
            )
        self.items[name] = Line(price, have + quantity)

    def remove(self, name: str) -> None:
        if name not in self.items:
            raise UnknownItem(f"{name} is not in the cart")
        del self.items[name]

    def subtotal(self) -> int:
        lines = self.items.values()
        return sum(ln.price * ln.quantity for ln in lines)

    def apply_coupon(self, code: str) -> None:
        if code not in COUPONS:
            raise InvalidCoupon(f"no coupon called {code}")
        self.coupon = COUPONS[code]

    def discount(self) -> int:
        coupon, subtotal = self.coupon, self.subtotal()
        if coupon is None or subtotal < coupon.minimum:
            return 0
        if coupon.kind == "percent":
            return subtotal * coupon.value // 100
        return min(coupon.value, subtotal)

    def tax(self) -> int:
        taxable = self.subtotal() - self.discount()
        return (taxable * GST_PERCENT + 50) // 100

    def total(self) -> int:
        return self.subtotal() - self.discount() + self.tax()

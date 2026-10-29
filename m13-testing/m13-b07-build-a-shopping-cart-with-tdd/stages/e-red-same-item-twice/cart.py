class Cart:
    def __init__(self) -> None:
        self.items: dict[str, tuple[int, int]] = {}

    def add(self, name: str, price: int, quantity: int = 1) -> None:
        self.items[name] = (price, quantity)

    def subtotal(self) -> int:
        return sum(p * q for p, q in self.items.values())

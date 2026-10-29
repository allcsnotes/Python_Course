class Cart:
    def __init__(self) -> None:
        self.items: dict[str, tuple[int, int]] = {}

    def add(self, name: str, price: int, quantity: int = 1) -> None:
        have = self.items[name][1] if name in self.items else 0
        self.items[name] = (price, have + quantity)

    def subtotal(self) -> int:
        return sum(p * q for p, q in self.items.values())

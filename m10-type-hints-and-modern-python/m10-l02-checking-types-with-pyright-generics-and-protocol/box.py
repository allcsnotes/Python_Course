class Box[T]:
    def __init__(self, item: T) -> None:
        self.item = item

    def get(self) -> T:
        return self.item


title_box = Box("Python")
price_box = Box(999)
reveal_type(title_box)
reveal_type(price_box.get())

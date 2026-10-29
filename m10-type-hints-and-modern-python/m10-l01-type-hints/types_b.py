def price_with_gst(price: int, rate: float = 0.18) -> float:
    return price * (1 + rate)


def show(name: str) -> None:
    print("Course:", name)


print(price_with_gst(1000))
result = show("Python Basics")
print(result)

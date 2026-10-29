def discount(price: int, percent: int) -> int:
    return price - price * percent // 100


print(discount("999", 10))  # type: ignore

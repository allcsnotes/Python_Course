def full_price(price: int, gst: float = 0.18) -> float:
    return price * (1 + gst)


def first_word(text: str) -> str | None:
    words = text.split()
    return words[0] if words else None


print(full_price(500))
print(first_word("Type hints are notes"))
print(first_word(""))
print(full_price("500"))

def label(price: int | str) -> str:
    reveal_type(price)
    if isinstance(price, str):
        reveal_type(price)
        return price.upper()
    reveal_type(price)
    return f"Rs {price}"

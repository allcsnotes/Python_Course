def final_price(price: int, coupon: str) -> int:
    """Price in whole rupees after a coupon code."""
    if coupon == "":
        return price
    if coupon == "HALF":
        return price // 2
    if coupon == "FLAT100":
        return price - 100
    raise ValueError(f"unknown coupon: {coupon}")


def bundle_total(price: int, quantity: int) -> int:
    """Buy three or more courses and get ten percent off."""
    total = price * quantity
    if quantity >= 3:
        total = total - total // 10
    return total

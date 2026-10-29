def digit_sum(n):
    """Add up the digits of a whole number."""
    if n < 10:
        return n
    return n % 10 + digit_sum(n // 10)


help(digit_sum)

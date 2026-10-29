def digit_sum(n):
    """Add up the digits of a whole number.

    digit_sum(4321) gives 10.
    """
    if n < 10:
        return n
    return n % 10 + digit_sum(n // 10)


print(digit_sum(4321))

import secrets
import string

ALPHABET = (
    string.digits
    + string.ascii_lowercase
    + string.ascii_uppercase
)
LENGTH = 7


def encode(number):
    """Write a number in base 62, like 125 -> '21'."""
    if number == 0:
        return ALPHABET[0]
    digits = []
    while number > 0:
        number, rest = divmod(number, 62)
        digits.append(ALPHABET[rest])
    return "".join(reversed(digits))


def new_code(length=LENGTH):
    return "".join(
        secrets.choice(ALPHABET) for _ in range(length)
    )

def read_amount(text):
    try:
        return float(text)
    except ValueError as error:
        raise ValueError("not a number") from error


print(read_amount("abc"))

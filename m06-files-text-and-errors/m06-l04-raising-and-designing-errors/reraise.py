def read_amount(text):
    try:
        return float(text)
    except ValueError:
        print("Log: bad amount", text)
        raise


print(read_amount("abc"))

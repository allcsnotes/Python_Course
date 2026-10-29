def set_percent(value):
    if value < 0 or value > 100:
        raise ValueError(f"percent must be 0 to 100, got {value}")
    return value


for value in [40, 150]:
    try:
        print("Saved", set_percent(value))
    except ValueError as error:
        print("Could not save:", error)

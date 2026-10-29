def is_broken(status):
    return status >= 400


def broken_only(statuses):
    return [s for s in statuses if is_broken(s)]


def describe(status):
    if status < 100 or status > 599:
        raise ValueError(f"not a real status: {status}")
    if is_broken(status):
        return "broken"
    return "fine"

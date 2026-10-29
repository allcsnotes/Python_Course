def _fix(title):
    title = title.lower()
    chars = [c if c.isalnum() else " " for c in title]
    return "".join(chars)


def slugify(title):
    return "-".join(_fix(title).split())

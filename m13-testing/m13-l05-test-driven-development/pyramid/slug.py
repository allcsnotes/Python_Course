def slugify(title):
    title = title.lower()
    chars = [c if c.isalnum() else " " for c in title]
    words = "".join(chars).split()
    if not words:
        raise ValueError("no letters or digits")
    return "-".join(words)

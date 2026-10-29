def slugify(title):
    title = title.lower()
    chars = [c if c.isalnum() else " " for c in title]
    words = "".join(chars).split()
    return "-".join(words)

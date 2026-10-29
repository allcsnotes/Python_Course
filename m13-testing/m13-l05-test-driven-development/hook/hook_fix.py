def slugify(title):
    text = title.lower()
    chars = [c if c.isalnum() else "-" for c in text]
    return "".join(chars)


print(slugify("C++ Basics!"))

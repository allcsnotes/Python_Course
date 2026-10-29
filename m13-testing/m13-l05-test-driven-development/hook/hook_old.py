def slugify(title):
    return "-".join(title.lower().split())


print(slugify("C++ Basics!"))

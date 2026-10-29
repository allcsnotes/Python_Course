def slugify(title):
    slug = title.lower()
    for mark in "+!":
        slug = slug.replace(mark, "")
    return "-".join(slug.split())

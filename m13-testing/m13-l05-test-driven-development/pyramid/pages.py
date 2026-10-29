from slug import slugify


def save_page(folder, title, text):
    path = folder / (slugify(title) + ".html")
    path.write_text(text)
    return path

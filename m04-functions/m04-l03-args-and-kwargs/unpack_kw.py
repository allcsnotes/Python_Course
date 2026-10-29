def label(title, price):
    return f"{title} costs Rs {price}"

course = {"title": "Python Basics", "price": 1499}
print(label(**course))

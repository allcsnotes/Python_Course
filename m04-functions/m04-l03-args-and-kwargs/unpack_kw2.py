def show_course(**details):
    for name, value in details.items():
        print(f"{name}: {value}")

course = {"title": "Python Basics", "price": 1499}
show_course(**course)

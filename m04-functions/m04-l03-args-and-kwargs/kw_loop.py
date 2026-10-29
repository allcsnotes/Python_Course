def show_course(**details):
    for name, value in details.items():
        print(f"{name}: {value}")

show_course(title="Python Basics", price=1499,
            level="beginner")

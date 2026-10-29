catalog = {
    "Python": {"price": 1499, "level": "beginner"},
    "SQL": {"price": 999, "level": "intermediate"},
    "Docker": {"price": 799, "level": "beginner"},
}
for name, info in catalog.items():
    print(name, info["level"], info["price"])

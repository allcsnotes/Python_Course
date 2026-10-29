catalog = {
    "Python": {"price": 1499, "level": "beginner"},
    "SQL": {"price": 999, "level": "intermediate"},
    "Docker": {"price": 799, "level": "beginner"},
}
print(catalog["SQL"])
print(catalog["SQL"]["price"])
catalog["SQL"]["price"] = 899
print(catalog["SQL"]["price"])

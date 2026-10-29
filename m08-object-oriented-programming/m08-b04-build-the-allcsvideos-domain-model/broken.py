from domain import Course

bad = [
    {"title": "Gift", "price": -499, "level": "beginner"},
    {"title": "Quiz", "price": 99, "level": "expert"},
]
for item in bad:
    item["lessons"] = []
    item["students"] = []
    try:
        Course.from_dict(item)
    except ValueError as err:
        print("Refused:", err)

events = [
    {"type": "enrolled", "student": {"name": "Lukas"}},
    {"type": "enrolled", "student": "Asha"},
    {"type": "paid", "student": {"name": "Priya"}},
]
for event in events:
    match event:
        case {"type": "enrolled", "student": {"name": who}}:
            print("enrolled:", who)
        case {"type": "paid", "student": {"name": who}}:
            print("paid:", who)
        case _:
            print("skipped:", event)

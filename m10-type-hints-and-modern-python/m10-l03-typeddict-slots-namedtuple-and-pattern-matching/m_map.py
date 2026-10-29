def handle(event):
    match event:
        case {"type": "enrolled", "student": name}:
            return f"{name} enrolled"
        case {"type": "paid", "amount": amount}:
            return f"paid {amount} rupees"
        case {"type": "refund"}:
            return "refund started"
        case _:
            return "unknown event"


events = [
    {"type": "enrolled", "student": "Lukas", "course": "C101"},
    {"type": "paid", "amount": 1499},
    {"type": "paid"},
    {"type": "refund", "amount": 499},
]
for event in events:
    print(handle(event))

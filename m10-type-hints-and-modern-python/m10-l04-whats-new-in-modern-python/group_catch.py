def send_all(emails):
    errors = []
    for email in emails:
        if "@" not in email:
            errors.append(ValueError(f"bad: {email}"))
        elif email.endswith(".xx"):
            errors.append(TimeoutError(f"slow: {email}"))
    if errors:
        raise ExceptionGroup("mail failed", errors)

emails = ["asha@x.com", "lukas.com", "priya@y.xx", "meera"]

try:
    send_all(emails)
except* ValueError as group:
    print("bad addresses:", len(group.exceptions))
    for error in group.exceptions:
        print(" ", error)
except* TimeoutError as group:
    print("slow servers:", len(group.exceptions))

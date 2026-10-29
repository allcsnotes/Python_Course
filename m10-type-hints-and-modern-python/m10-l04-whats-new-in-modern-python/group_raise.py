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
send_all(emails)

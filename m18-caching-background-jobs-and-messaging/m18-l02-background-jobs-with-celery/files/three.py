from tasks import send_welcome_email

for name in ("lukas", "priya", "asha"):
    send_welcome_email.delay(f"{name}@example.com", "Python Basics")
print("three tasks queued")

def send_welcome_email(student):
    print(f"email sent to {student}")


def update_stats(course):
    print(f"stats updated for {course}")


def notify_dashboard(course):
    raise ConnectionError("dashboard is down")


def enroll(student, course):
    print(f"saved {student} in {course}")
    send_welcome_email(student)
    update_stats(course)
    notify_dashboard(course)
    print("enrolled!")


enroll("Lukas", "python-basics")

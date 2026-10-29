from app.worker import send_welcome_email

JOB = {
    "student_id": 1,
    "course_id": 1,
    "name": "Priya",
    "email": "priya@example.com",
    "title": "Python Basics",
}

send_welcome_email.delay(**JOB)
send_welcome_email.delay(**JOB)
print("queued the same job twice")

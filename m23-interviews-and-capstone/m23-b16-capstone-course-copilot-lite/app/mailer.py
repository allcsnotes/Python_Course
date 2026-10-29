import smtplib
from email.message import EmailMessage

from app.settings import get_settings


def progress_message(name, email, done, total):
    settings = get_settings()
    message = EmailMessage()
    message["Subject"] = (
        f"Your week: {done} of {total} lessons"
    )
    message["From"] = settings.mail_from
    message["To"] = email
    message.set_content(
        f"Hi {name},\n\n"
        f"You have finished {done} of {total} lessons.\n"
        "Keep going: one lesson a day adds up.\n\n"
        "Course Copilot-lite"
    )
    return message


def send(message):
    settings = get_settings()
    with smtplib.SMTP(
        settings.smtp_host, settings.smtp_port, timeout=5
    ) as server:
        server.send_message(message)

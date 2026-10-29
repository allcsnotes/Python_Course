import smtplib
from email.message import EmailMessage

from opentelemetry import trace

from app.settings import get_settings

tracer = trace.get_tracer("allcs.mailer")
SMTP_HOST = get_settings().smtp_host
SMTP_PORT = get_settings().smtp_port


def welcome_message(name, email, title):
    message = EmailMessage()
    message["From"] = "hello@allcsvideos.com"
    message["To"] = email
    message["Subject"] = f"Welcome to {title}"
    message.set_content(
        f"Hi {name},\n\n"
        f"You are enrolled in {title}.\n"
        "Your first lesson is ready.\n\n"
        "The allcsvideos team\n"
    )
    return message


def send(message):
    with tracer.start_as_current_span("smtp.send") as span:
        span.set_attribute("smtp.host", SMTP_HOST)
        with smtplib.SMTP(
            SMTP_HOST, SMTP_PORT, timeout=5
        ) as smtp:
            smtp.send_message(message)

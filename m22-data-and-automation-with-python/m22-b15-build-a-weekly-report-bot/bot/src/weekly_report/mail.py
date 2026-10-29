import smtplib
from email.message import EmailMessage

KINDS = {
    ".pdf": "pdf",
    ".xlsx": "vnd.openxmlformats-officedocument.spreadsheetml.sheet",
}


def make_message(settings, subject, body, to, files=()):
    message = EmailMessage()
    message["From"] = settings.mail_from
    message["To"] = to
    message["Subject"] = subject
    message.set_content(body)
    for path in files:
        message.add_attachment(
            path.read_bytes(),
            maintype="application",
            subtype=KINDS[path.suffix],
            filename=path.name,
        )
    return message


def send(settings, message):
    host, port = settings.smtp_host, settings.smtp_port
    with smtplib.SMTP(host, port, timeout=10) as smtp:
        smtp.send_message(message)

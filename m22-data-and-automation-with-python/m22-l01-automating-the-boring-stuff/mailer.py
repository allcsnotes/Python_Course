import os
import smtplib
from email.message import EmailMessage
from pathlib import Path

XLSX = "vnd.openxmlformats-officedocument.spreadsheetml.sheet"


def send_report(report: Path, to: str) -> None:
    msg = EmailMessage()
    msg["From"] = "asha@allcsvideos.com"
    msg["To"] = to
    msg["Subject"] = "Weekly report: 19 to 25 October"
    msg.set_content("Hi Meera,\n\nThe weekly report is attached.\n\nAsha")
    msg.add_attachment(report.read_bytes(), maintype="application",
                       subtype=XLSX, filename=report.name)
    host = os.environ["SMTP_HOST"]
    port = int(os.environ["SMTP_PORT"])
    user = os.environ["SMTP_USER"]
    password = os.environ["SMTP_PASSWORD"]
    with smtplib.SMTP(host, port, timeout=10) as server:
        server.login(user, password)
        server.send_message(msg)

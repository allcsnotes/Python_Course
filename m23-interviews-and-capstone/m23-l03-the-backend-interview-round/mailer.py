import os
import time


class SendError(OSError):
    pass


def send_mail(cert_id):
    """Stand-in for the mail server: fails while a flag file says so."""
    if os.path.exists("mail_down"):
        raise SendError("mail server not answering")
    with open("sent_mail.txt", "a") as out:
        out.write(f"certificate {cert_id} {time.time():.0f}\n")

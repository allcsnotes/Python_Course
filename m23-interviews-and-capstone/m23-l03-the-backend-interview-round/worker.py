import os

import psycopg
from celery import Celery

from mailer import SendError, send_mail

DSN = os.environ.get(
    "DATABASE_URL",
    "postgresql://postgres:demo@localhost:23503/allcs",
)
PORT = os.environ.get("REDIS_PORT", "23403")
app = Celery("enroll", broker=f"redis://localhost:{PORT}/1")


@app.task(
    bind=True,
    autoretry_for=(SendError,),
    retry_backoff=1,
    retry_jitter=False,
    max_retries=4,
)
def send_certificate(self, cert_id):
    with psycopg.connect(DSN) as db:
        row = db.execute(
            "SELECT status FROM certificates"
            " WHERE id = %s", (cert_id,)
        ).fetchone()
        if row[0] == "sent":
            return "already sent"
        db.execute(
            "UPDATE certificates"
            " SET attempts = attempts + 1"
            " WHERE id = %s", (cert_id,)
        )
        db.commit()
        send_mail(cert_id)
        db.execute(
            "UPDATE certificates"
            " SET status = 'sent', sent_at = now()"
            " WHERE id = %s", (cert_id,)
        )
    return "sent"

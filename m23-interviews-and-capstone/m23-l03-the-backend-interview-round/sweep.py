import psycopg

from worker import DSN, send_certificate

with psycopg.connect(DSN) as db:
    rows = db.execute(
        "SELECT id FROM certificates WHERE status = 'pending'"
        " AND created_at < now() - interval '2 seconds'"
    ).fetchall()
for (cert_id,) in rows:
    send_certificate.delay(cert_id)
    print("queued again:", cert_id)

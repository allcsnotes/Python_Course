import json
import sqlite3

from confluent_kafka import Producer

from bus import KAFKA, topic_size
from events import enrolled

db = sqlite3.connect("allcs2.db")
db.execute("CREATE TABLE enrollments (student TEXT, course TEXT)")
db.execute("CREATE TABLE outbox (id TEXT, body TEXT, sent INT)")
producer = Producer({"bootstrap.servers": KAFKA})


def enroll(student, course):
    event = enrolled(student, course)
    with db:
        db.execute("INSERT INTO enrollments VALUES (?, ?)",
                   (student, course))
        db.execute("INSERT INTO outbox VALUES (?, ?, 0)",
                   (event["id"], json.dumps(event)))


def relay():
    rows = db.execute("SELECT id, body FROM outbox WHERE sent = 0")
    for event_id, body in rows.fetchall():
        producer.produce("enrollments", body)
        producer.flush()
        with db:
            db.execute("UPDATE outbox SET sent = 1 WHERE id = ?",
                       (event_id,))


enroll("Lukas", "python-basics")
pending = "SELECT COUNT(*) FROM outbox WHERE sent = 0"
print("waiting in the outbox:", db.execute(pending).fetchone()[0])
print("events in the topic:", topic_size("enrollments"))
relay()
print("waiting in the outbox:", db.execute(pending).fetchone()[0])
print("events in the topic:", topic_size("enrollments"))

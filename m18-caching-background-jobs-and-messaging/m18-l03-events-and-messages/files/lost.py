import json
import sqlite3

from confluent_kafka import Producer

from bus import KAFKA, topic_size
from events import enrolled

db = sqlite3.connect("allcs.db")
db.execute("CREATE TABLE enrollments (student TEXT, course TEXT)")
producer = Producer({"bootstrap.servers": KAFKA})


def enroll(student, course, crash=False):
    db.execute("INSERT INTO enrollments VALUES (?, ?)",
               (student, course))
    db.commit()
    if crash:
        raise SystemExit("power cut before publish!")
    event = enrolled(student, course)
    producer.produce("enrollments", json.dumps(event))
    producer.flush()


try:
    enroll("Lukas", "python-basics", crash=True)
except SystemExit as stop:
    print(stop)
rows = db.execute("SELECT COUNT(*) FROM enrollments")
print("enrollments saved:", rows.fetchone()[0])
print("events in the topic:", topic_size("enrollments"))

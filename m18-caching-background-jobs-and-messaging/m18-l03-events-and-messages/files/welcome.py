import json
import os

from confluent_kafka import Consumer

from bus import KAFKA

consumer = Consumer({
    "bootstrap.servers": KAFKA,
    "group.id": "welcome",
    "auto.offset.reset": "earliest",
    "enable.auto.commit": False,
})
consumer.subscribe(["enrollments"])


def handle(e):
    print("welcome email to", e["student"], e["course"])


try:
    while (msg := consumer.poll(5)) is not None:
        e = json.loads(msg.value())
        handle(e)
        if e["id"] == os.environ.get("CRASH_ON"):
            raise SystemExit("power cut before the commit!")
        consumer.commit(msg)
finally:
    consumer.close()

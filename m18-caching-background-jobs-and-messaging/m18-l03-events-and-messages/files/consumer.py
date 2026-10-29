import json
import sys

from confluent_kafka import Consumer

from bus import KAFKA

group = sys.argv[1]
consumer = Consumer({
    "bootstrap.servers": KAFKA,
    "group.id": group,
    "auto.offset.reset": "earliest",
    "enable.auto.commit": False,
})
consumer.subscribe(["enrollments"])
while (msg := consumer.poll(5)) is not None:
    e = json.loads(msg.value())
    print(group, "offset", msg.offset(), e["student"], e["course"])
    consumer.commit(msg)
print(group, "is up to date")
consumer.close()

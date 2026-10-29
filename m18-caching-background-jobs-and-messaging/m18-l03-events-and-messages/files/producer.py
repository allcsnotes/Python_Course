import json
import sys

from confluent_kafka import Producer

from bus import KAFKA
from events import enrolled

producer = Producer({"bootstrap.servers": KAFKA})
course = sys.argv[1]
for student in sys.argv[2:]:
    event = enrolled(student, course)
    producer.produce("enrollments", json.dumps(event))
producer.flush()
print("events sent:", len(sys.argv) - 2)

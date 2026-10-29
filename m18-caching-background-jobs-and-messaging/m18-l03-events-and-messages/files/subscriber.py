import json
import sys

from bus import r


def show(name, data):
    e = json.loads(data)
    print(name, "got", e["student"], e["course"], flush=True)


name = sys.argv[1]
sub = r.pubsub()
sub.subscribe("enrollments")
print(name, "is listening", flush=True)
try:
    for msg in sub.listen():
        if msg["type"] == "message":
            show(name, msg["data"])
except KeyboardInterrupt:
    print(name, "stopped")

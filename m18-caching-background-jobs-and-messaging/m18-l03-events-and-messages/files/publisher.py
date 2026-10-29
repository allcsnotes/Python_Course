import json
import sys

from bus import r
from events import enrolled

course = sys.argv[1]
for student in sys.argv[2:]:
    event = enrolled(student, course)
    count = r.publish("enrollments", json.dumps(event))
    print(f"published {student}: received by {count}")

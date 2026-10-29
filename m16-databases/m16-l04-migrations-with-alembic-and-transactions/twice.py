import threading
import time

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from db import engine
from models import Enrollment


def enrol(name):
    with Session(engine) as s:
        already = s.get(Enrollment, (1, 1))
        if already is None:
            time.sleep(0.5)  # the payment, the email
            s.add(Enrollment(student_id=1, course_id=1))
            try:
                s.commit()
                print(name, "enrolled Lukas")
            except IntegrityError:
                print(name, "too late: the database said no")
        else:
            print(name, "found him already enrolled")


clicks = [threading.Thread(target=enrol, args=(n,))
          for n in ("click 1", "click 2")]
for c in clicks:
    c.start()
for c in clicks:
    c.join()

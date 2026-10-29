import time

from toolkit import timed


@timed
def broken_report():
    time.sleep(0.1)
    raise ValueError("no data for today")


try:
    broken_report()
except ValueError as error:
    print("caught:", error)

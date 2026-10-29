import time

from toolkit import timed


@timed
def load_report(day):
    """Build the daily report."""
    time.sleep(0.2)
    return f"report for {day}"


print(load_report("Monday"))
print(load_report.__name__)
print(load_report.__doc__)

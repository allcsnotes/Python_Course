import time


def load_report():
    start = time.perf_counter()
    time.sleep(0.2)
    ms = (time.perf_counter() - start) * 1000
    print(f"load_report took {ms:.0f} ms")
    return "daily report"


def load_students():
    start = time.perf_counter()
    time.sleep(0.1)
    ms = (time.perf_counter() - start) * 1000
    print(f"load_students took {ms:.0f} ms")
    return ["Priya", "Lukas"]


print(load_report())
print(load_students())

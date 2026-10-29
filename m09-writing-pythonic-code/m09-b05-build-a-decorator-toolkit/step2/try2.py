from toolkit import RetryableError, retry

state = {"calls": 0}


@retry(times=3, delay=0.1)
def load_catalog():
    state["calls"] += 1
    if state["calls"] < 3:
        raise RetryableError("server busy")
    return ["Python Basics", "Loops"]


print(load_catalog())
print("calls:", state["calls"])

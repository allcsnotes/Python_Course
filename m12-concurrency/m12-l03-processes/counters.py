def add_unsafe(counter):
    for _ in range(50_000):
        counter.value += 1


def add_safe(counter):
    for _ in range(50_000):
        with counter.get_lock():
            counter.value += 1

import time


class Timer:
    def __enter__(self):
        self.start = time.perf_counter()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.seconds = time.perf_counter() - self.start


with Timer() as timer:
    time.sleep(0.2)
print("took", round(timer.seconds, 1), "seconds")

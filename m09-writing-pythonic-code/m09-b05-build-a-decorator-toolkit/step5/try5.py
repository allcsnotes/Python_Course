from toolkit import RetryableError, retry, timed

tries = {"one": 0, "two": 0}


def flaky(name):
    tries[name] += 1
    if tries[name] < 3:
        raise RetryableError("server busy")


@timed
@retry(times=3, delay=0.1)
def load_one():
    flaky("one")


@retry(times=3, delay=0.1)
@timed
def load_two():
    flaky("two")


load_one()
load_two()

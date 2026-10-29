import pytest

from retry import retry


class Flaky:
    def __init__(self, failures, error=ConnectionError):
        self.failures, self.error, self.calls = failures, error, 0

    def __call__(self):
        self.calls += 1
        if self.calls <= self.failures:
            raise self.error("down")
        return "ok"


def test_succeeds_first_time_without_sleeping():
    slept = []
    func = retry(sleep=slept.append)(Flaky(0))
    assert func() == "ok" and slept == []


def test_retries_with_growing_waits():
    slept = []
    flaky = Flaky(2)
    func = retry(times=4, delay=1, factor=3, sleep=slept.append)(flaky)
    assert func() == "ok"
    assert flaky.calls == 3 and slept == [1, 3]


def test_gives_up_and_reraises_the_last_error():
    slept = []
    flaky = Flaky(10)
    with pytest.raises(ConnectionError):
        retry(times=3, sleep=slept.append)(flaky)()
    assert flaky.calls == 3 and len(slept) == 2     # no sleep after the final failure


def test_other_errors_are_not_retried():
    flaky = Flaky(5, error=KeyError)
    with pytest.raises(KeyError):
        retry(times=3, exceptions=(ConnectionError,), sleep=lambda s: None)(flaky)()
    assert flaky.calls == 1


def test_keeps_the_name_and_docstring():
    @retry()
    def fetch():
        "Fetch data."
    assert fetch.__name__ == "fetch" and fetch.__doc__ == "Fetch data."


def test_times_must_be_positive():
    with pytest.raises(ValueError):
        retry(times=0)

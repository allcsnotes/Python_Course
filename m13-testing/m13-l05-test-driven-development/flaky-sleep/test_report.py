import time

from report import Report


def test_report_is_ready():
    report = Report()
    report.start()
    time.sleep(0.05)
    assert report.ready

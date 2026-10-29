from report import Report


def test_report_is_ready():
    report = Report()
    worker = report.start()
    worker.join()
    assert report.ready

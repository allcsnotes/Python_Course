import logging

from enrol import enrol


def test_enrol_logs_info(caplog):
    with caplog.at_level(logging.INFO):
        enrol([], "Lukas")
    assert "enrolled Lukas" in caplog.text


def test_double_enrol_warns(caplog):
    enrol(["Lukas"], "Lukas")
    assert caplog.records[0].levelname == "WARNING"

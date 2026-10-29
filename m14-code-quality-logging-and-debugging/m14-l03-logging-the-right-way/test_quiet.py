from enrol import enrol


def test_enrol_logs_info(caplog):
    enrol([], "Lukas")
    assert "enrolled Lukas" in caplog.text

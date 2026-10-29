import time

import pytest


@pytest.mark.slow
def test_big_report():
    time.sleep(1.2)
    assert sum(range(5)) == 10

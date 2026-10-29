from linkrules import broken_only


def test_keeps_the_bad_ones():
    statuses = [200, 301, 404, 500, 400]
    result = broken_only(statuses)
    assert result == [404, 500, 400]

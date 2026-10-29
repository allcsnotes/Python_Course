from linkrules import is_broken


def test_404_is_broken():
    assert is_broken(404)


def check_500_is_broken():
    assert is_broken(500)

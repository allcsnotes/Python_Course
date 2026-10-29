from linkrules import is_broken


def test_404_is_broken():
    assert is_broken(404)

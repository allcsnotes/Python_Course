from linkrules import is_broken


def test_404_is_broken():
    assert is_broken(404)


def test_200_is_fine():
    assert not is_broken(200)


def test_400_is_broken():
    assert is_broken(400)

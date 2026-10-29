from linkrules import is_broken


def test_400_is_broken():
    is_broken(400) == True

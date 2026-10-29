users = []


def test_sign_up():
    users.append("Priya")
    assert users == ["Priya"]


def test_one_user_signed_up():
    assert len(users) == 1

def test_sign_up():
    users = []
    users.append("Priya")
    assert users == ["Priya"]


def test_one_user_signed_up():
    users = ["Priya"]
    assert len(users) == 1

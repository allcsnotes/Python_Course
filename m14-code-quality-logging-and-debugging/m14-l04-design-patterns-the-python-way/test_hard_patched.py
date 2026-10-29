import checkout_hard


class Fake:
    def charge(self, student, amount):
        return "fake: ok"


def test_checkout(monkeypatch):
    monkeypatch.setattr(checkout_hard, "CardGateway", Fake)
    receipt = checkout_hard.checkout("Priya", 590)
    assert receipt == "fake: ok"

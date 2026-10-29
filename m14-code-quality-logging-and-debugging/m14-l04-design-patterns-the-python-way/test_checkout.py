from checkout import checkout


class FakeGateway:
    def __init__(self):
        self.charges = []

    def charge(self, student, amount):
        self.charges.append((student, amount))
        return "fake: ok"


def test_checkout_charges_once():
    gateway = FakeGateway()
    receipt = checkout("Priya", 590, gateway)
    assert receipt == "fake: ok"
    assert gateway.charges == [("Priya", 590)]

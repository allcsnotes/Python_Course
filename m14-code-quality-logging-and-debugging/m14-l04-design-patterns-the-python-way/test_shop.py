from events import OrderEvents
from shop import place_order


class FakeGateway:
    def __init__(self):
        self.charges = []

    def charge(self, student, amount):
        self.charges.append((student, amount))


def test_place_order():
    fake, seen = FakeGateway(), []
    events = OrderEvents()
    events.subscribe(lambda *args: seen.append(args))
    place_order("Priya", 500, lambda p: p - 50, fake, events)
    assert fake.charges == [("Priya", 450)]
    assert seen == [("Priya", 450)]

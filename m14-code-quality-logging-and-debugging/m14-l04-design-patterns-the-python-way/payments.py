import time


class CardGateway:
    def charge(self, student, amount):
        time.sleep(0.5)  # pretend bank: 0.5 s
        return f"card: charged {student} Rs {amount}"


class UpiGateway:
    def charge(self, student, amount):
        time.sleep(0.5)  # pretend bank: 0.5 s
        return f"upi: charged {student} Rs {amount}"


GATEWAYS = {"card": CardGateway, "upi": UpiGateway}


def make_gateway(kind):
    if kind not in GATEWAYS:
        raise ValueError(f"unknown payment kind: {kind}")
    return GATEWAYS[kind]()

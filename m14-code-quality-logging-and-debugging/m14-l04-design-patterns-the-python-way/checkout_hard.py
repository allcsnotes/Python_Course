from payments import CardGateway


def checkout(student, price):
    gateway = CardGateway()
    return gateway.charge(student, price)

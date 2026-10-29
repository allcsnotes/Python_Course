def place_order(student, price, discount, gateway, events):
    amount = discount(price)
    receipt = gateway.charge(student, amount)
    events.publish(student, amount)
    return receipt

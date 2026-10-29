class OrderEvents:
    def __init__(self):
        self.listeners = []

    def subscribe(self, listener):
        self.listeners.append(listener)

    def publish(self, student, amount):
        for listener in self.listeners:
            listener(student, amount)

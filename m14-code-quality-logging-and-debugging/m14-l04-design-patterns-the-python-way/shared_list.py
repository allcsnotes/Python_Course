class Events:
    listeners = []

    def subscribe(self, listener):
        self.listeners.append(listener)


first = Events()
second = Events()
first.subscribe(print)
print(len(second.listeners))

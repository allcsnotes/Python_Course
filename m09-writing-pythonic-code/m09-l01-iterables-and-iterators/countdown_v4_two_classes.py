class Countdown:
    def __init__(self, start):
        self.start = start

    def __iter__(self):
        return CountdownWalker(self.start)


class CountdownWalker:
    def __init__(self, current):
        self.current = current

    def __iter__(self):
        return self

    def __next__(self):
        if self.current == 0:
            raise StopIteration
        value = self.current
        self.current -= 1
        return value


timer = Countdown(3)
for number in timer:
    print(number)
print("--- again ---")
for number in timer:
    print(number)

class Countdown:
    def __init__(self, start):
        self.start = start

    def __iter__(self):
        return iter(range(self.start, 0, -1))


timer = Countdown(3)
for number in timer:
    print(number)
print("--- again ---")
for number in timer:
    print(number)

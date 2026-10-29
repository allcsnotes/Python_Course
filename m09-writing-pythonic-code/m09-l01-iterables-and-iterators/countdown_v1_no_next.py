class Countdown:
    def __init__(self, start):
        self.current = start

    def __iter__(self):
        return self


for number in Countdown(3):
    print(number)

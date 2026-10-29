from abc import abstractmethod


class Payment:
    @abstractmethod
    def pay(self, amount):
        pass


payment = Payment()
print("Created with no error")

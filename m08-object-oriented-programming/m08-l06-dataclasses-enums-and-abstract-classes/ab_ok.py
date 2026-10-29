from abc import ABC, abstractmethod


class Payment(ABC):
    @abstractmethod
    def pay(self, amount):
        pass


class UpiPayment(Payment):
    def pay(self, amount):
        print(f"Paid Rs {amount} by UPI")


class CardPayment(Payment):
    def pay(self, amount):
        print(f"Paid Rs {amount} by card")


for method in [UpiPayment(), CardPayment()]:
    method.pay(2499)

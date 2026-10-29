from abc import ABC, abstractmethod


class Payment(ABC):
    @abstractmethod
    def pay(self, amount):
        pass


class CardPayment(Payment):
    def charge(self, amount):
        print(f"Charged Rs {amount}")


CardPayment().pay(2499)
print("Order confirmed")

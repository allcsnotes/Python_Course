# Exercise 09 - Predict the output (underscore, double underscore, property)
class Wallet:
    def __init__(self, owner, balance):
        self.owner = owner
        self.__pin = "4821"
        self._balance = balance

    @property
    def balance(self):
        return self._balance

    @balance.setter
    def balance(self, value):
        if value < 0:
            raise ValueError(f"balance cannot be negative, got {value}")
        self._balance = value


wallet = Wallet("Priya", 500)
print(wallet.owner, wallet.balance)
wallet.balance = 700
print(wallet.balance)
try:
    wallet.balance = -1
except ValueError as error:
    print("Error:", error)
print(wallet.balance)
wallet._balance = -50
print(wallet.balance)
try:
    print(wallet.__pin)
except AttributeError as error:
    print("Error:", error)
print(wallet._Wallet__pin)
print(vars(wallet))

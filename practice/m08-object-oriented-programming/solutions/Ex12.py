# Exercise 12 - Predict the output (method lookup order and error families)
class Person:
    def role(self):
        return "member"


class Student(Person):
    def role(self):
        return "learns"


class Instructor(Person):
    def role(self):
        return "teaches"


class TeachingAssistant(Student, Instructor):
    pass


class Visitor(Person):
    pass


priya = TeachingAssistant()
print(priya.role())
print([c.__name__ for c in TeachingAssistant.__mro__])
print(Visitor().role())
print(isinstance(priya, Instructor), isinstance(priya, Visitor))


class PaymentError(Exception):
    pass


class CardDeclinedError(PaymentError):
    pass


class UpiTimeoutError(PaymentError):
    pass


def pay(kind):
    if kind == "card":
        raise CardDeclinedError("card was declined")
    if kind == "upi":
        raise UpiTimeoutError("upi timed out")
    return "paid"


for kind in ["cash", "card", "upi"]:
    try:
        print(pay(kind))
    except CardDeclinedError as error:
        print("Declined:", error)
    except PaymentError as error:
        print("Other payment problem:", error)

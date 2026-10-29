class PaymentError(Exception):
    pass


class CardDeclinedError(PaymentError):
    pass


def pay(card_ok):
    if not card_ok:
        raise CardDeclinedError("card was declined")
    return "paid"


try:
    print(pay(True))
    print(pay(False))
except PaymentError as error:
    print("Payment problem:", error)

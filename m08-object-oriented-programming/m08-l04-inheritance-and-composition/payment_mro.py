class PaymentError(Exception):
    pass


class CardDeclinedError(PaymentError):
    pass


print([c.__name__ for c in CardDeclinedError.__mro__])

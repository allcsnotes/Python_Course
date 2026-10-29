class PaymentError(Exception):
    pass


raise PaymentError("card was declined")

def send_receipt(student, amount):
    print(f"email: receipt for {student}, Rs {amount}")


def count_sale(student, amount):
    print(f"stats: one more sale, Rs {amount}")


def send_sms(student, amount):
    raise ConnectionError("sms service is down")

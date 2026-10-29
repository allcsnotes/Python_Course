from Q16_app.mailer import send_email      # the name now lives HERE too


def welcome(student):
    send_email(student, "Welcome to allcsvideos")
    return "sent"

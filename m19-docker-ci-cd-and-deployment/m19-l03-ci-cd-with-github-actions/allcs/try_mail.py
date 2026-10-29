from app import mailer

message = mailer.welcome_message(
    "Lukas", "lukas@example.com", "Python Basics"
)
mailer.send(message)
print("sent to", message["To"])

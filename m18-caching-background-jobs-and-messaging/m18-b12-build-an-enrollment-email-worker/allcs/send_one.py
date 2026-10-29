import sys

from app import mailer

name, email, title = sys.argv[1:4]
mailer.send(mailer.welcome_message(name, email, title))

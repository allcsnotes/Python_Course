import os

SECRET_KEY = os.environ["SECRET_KEY"]
print("key loaded, length", len(SECRET_KEY))

class User:
    def is_admin(self):
        return False


user = User()
if user.is_admin:
    print("Welcome, admin")
else:
    print("Welcome, student")

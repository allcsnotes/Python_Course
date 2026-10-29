from app.settings import get_settings

s = get_settings()
print("access_seconds =", s.access_seconds)
print("secret_key     =", s.secret_key)

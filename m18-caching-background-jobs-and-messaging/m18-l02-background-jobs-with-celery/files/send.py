from tasks import send_welcome_email

result = send_welcome_email.delay("lukas@example.com", "Python Basics")
print("queued:", result.id)
print("state:", result.state)
print("answer:", result.get(timeout=10))
print("state:", result.state)

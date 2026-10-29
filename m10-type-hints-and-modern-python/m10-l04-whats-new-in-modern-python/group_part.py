errors = [ValueError("bad"), TimeoutError("slow")]
try:
    raise ExceptionGroup("mail failed", errors)
except* ValueError:
    print("handled the value errors")

errors = [ValueError("bad address")]
try:
    raise ExceptionGroup("mail failed", errors)
except ValueError:
    print("caught")

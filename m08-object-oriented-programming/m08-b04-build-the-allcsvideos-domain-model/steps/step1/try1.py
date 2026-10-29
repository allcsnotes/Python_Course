from domain import AlreadyEnrolledError, DomainError, Level

print(Level.BEGINNER)
print(Level("advanced"))
print([level.value for level in Level])

try:
    raise AlreadyEnrolledError("Priya enrolled twice")
except DomainError as err:
    print(type(err).__name__, "-", err)

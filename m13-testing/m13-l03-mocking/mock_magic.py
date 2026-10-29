from unittest.mock import MagicMock, Mock

try:
    with Mock() as plain:
        pass
except TypeError as error:
    print(error)
with MagicMock() as magic:
    print("MagicMock works with with")

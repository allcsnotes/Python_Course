from unittest.mock import Mock

from store import Gateway

loose = Mock()
loose.chrage("Priya", 590)
print("loose accepted the typo")
strict = Mock(spec=Gateway)
try:
    strict.chrage("Priya", 590)
except AttributeError as error:
    print(error)

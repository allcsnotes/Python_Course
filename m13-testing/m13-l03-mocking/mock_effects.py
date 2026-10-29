from unittest.mock import Mock

bank = Mock()
bank.charge.side_effect = [ConnectionError("busy"), "ok"]
try:
    bank.charge("Priya", 590)
except ConnectionError as error:
    print("first:", error)
print("second:", bank.charge("Priya", 590))

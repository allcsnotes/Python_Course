from unittest.mock import Mock

gateway = Mock()
gateway.charge.return_value = "ok"
print(gateway.charge("Priya", 590))
print(gateway.charge.call_count)
print(gateway.charge.call_args)
gateway.charge("Lukas", 590)
print(gateway.charge.call_args_list)

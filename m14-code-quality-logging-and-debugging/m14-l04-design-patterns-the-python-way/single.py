import config
import config as again

config.settings["currency"] = "USD"
print(again.settings["currency"])
print(config is again)

import json
from urllib.request import urlopen

with urlopen("http://localhost:22126/api/v1/messages") as r:
    print("messages in Mailpit:", json.load(r)["total"])

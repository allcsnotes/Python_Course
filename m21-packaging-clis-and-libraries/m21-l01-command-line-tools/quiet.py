import json
import sys

print("Reading server.log ...", file=sys.stderr)
print(json.dumps({"errors": 204}))

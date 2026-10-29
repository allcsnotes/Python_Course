import sys

import httpx

print(httpx.get(sys.argv[1] + "/whoami").json())

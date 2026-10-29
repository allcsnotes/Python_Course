import sys

from auth import make_token

print(make_token(int(sys.argv[1])))

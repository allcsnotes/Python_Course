import json
import sys
import urllib.parse
import urllib.request

URL = "http://localhost:20091/api/v1/query?"
query = urllib.parse.urlencode({"query": sys.argv[1]})
answer = json.load(urllib.request.urlopen(URL + query))
for row in answer["data"]["result"]:
    labels = ",".join(f'{k}="{v}"' for k, v in row["metric"].items())
    print("{" + labels + "}", round(float(row["value"][1]), 3))

import sys, json, urllib.request
t = sys.argv[1]
d = json.load(urllib.request.urlopen(f"http://localhost:20162/api/traces/{t}"))
for tr in d["data"]:
    ps = {p: v["serviceName"] for p, v in tr["processes"].items()}
    t0 = min(s["startTime"] for s in tr["spans"])
    for s in sorted(tr["spans"], key=lambda s: s["startTime"]):
        tags = {x["key"]: x["value"] for x in s["tags"]}
        print(f'{ps[s["processID"]]:12} {(s["startTime"]-t0)/1000:8.1f} {s["duration"]/1000:8.1f}  {s["operationName"][:70]}  {tags.get("db.statement", tags.get("db.query.text",""))[:70]}')

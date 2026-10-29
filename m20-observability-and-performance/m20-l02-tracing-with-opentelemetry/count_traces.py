import datetime as dt, json, urllib.request
f = lambda d: (dt.datetime.now(dt.UTC) + dt.timedelta(hours=d)).strftime('%Y-%m-%dT%H:%M:%SZ')
u = f"http://localhost:20162/api/v3/traces?query.service_name=allcs-api&query.operation_name=GET%20/courses&query.start_time_min={f(-1)}&query.start_time_max={f(1)}&query.search_depth=1000"
ids = set()
for line in urllib.request.urlopen(u).read().decode().splitlines():
    for rs in json.loads(line)['result']['resourceSpans']:
        for ss in rs['scopeSpans']:
            for sp in ss['spans']:
                if sp['name'] == 'GET /courses': ids.add(sp['traceId'])
print(len(ids))

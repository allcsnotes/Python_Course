import tracemalloc

report_cache = {}


def build_report(request_id):
    report = [request_id] * 1000
    report_cache[request_id] = report
    return len(report)


tracemalloc.start()
for request_id in range(1, 3001):
    build_report(request_id)
snapshot = tracemalloc.take_snapshot()
top = snapshot.statistics("lineno")[0]
print("line", top.traceback[0].lineno)
print(round(top.size / 1_000_000, 1), "MB")

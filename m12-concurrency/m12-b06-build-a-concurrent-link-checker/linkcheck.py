import json
import sys
import time
from dataclasses import asdict

import aio
import seq
import threaded
from core import BAD, LINKS, report


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "async"
    workers = int(sys.argv[2]) if len(sys.argv) > 2 else 8
    began = time.perf_counter()
    if mode == "seq":
        results = seq.run(LINKS)
    elif mode == "threads":
        results = threaded.run(LINKS, workers)
    elif mode == "async":
        results = aio.run(LINKS, workers)
    else:
        sys.exit(f"unknown mode: {mode}")
    report(results, time.perf_counter() - began)
    with open("report.json", "w") as file:
        json.dump([asdict(r) for r in results], file, indent=2)
    if any(r.kind in BAD for r in results):
        sys.exit(1)


if __name__ == "__main__":
    main()

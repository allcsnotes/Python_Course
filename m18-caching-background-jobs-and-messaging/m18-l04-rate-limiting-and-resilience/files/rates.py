# practice service: python rates.py slow|nap|flaky|outage|down|charge  (port 8284)
import json
import sys
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

MODE = sys.argv[1]
CALLS = 0
FIRST = None
CHARGES = []
SEEN = {}


class H(BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def send(self, code, body, extra=None):
        data = json.dumps(body).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        for k, v in (extra or {}).items():
            self.send_header(k, v)
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        global CALLS, FIRST
        if self.path == "/charges":
            return self.send(200, {"count": len(CHARGES)})
        CALLS += 1
        if FIRST is None:
            FIRST = time.monotonic()
        if MODE == "slow":
            time.sleep(4)
        elif MODE == "nap":
            time.sleep(1)
        elif MODE == "flaky" and CALLS <= 3:
            return self.send(503, {"error": "busy"})
        elif MODE == "outage" and time.monotonic() - FIRST < 2.8:
            return self.send(503, {"error": "down"})
        elif MODE == "down":
            return self.send(503, {"error": "down"})
        self.send(200, {"inr_per_eur": 90.5})

    def do_POST(self):
        n = int(self.headers.get("Content-Length") or 0)
        self.rfile.read(n)
        key = self.headers.get("Idempotency-Key")
        if key is None or key not in SEEN:
            CHARGES.append(key)
            SEEN[key] = len(CHARGES)
        time.sleep(1.5)
        self.send(200, {"charge": SEEN[key]})


ThreadingHTTPServer(("127.0.0.1", 8284), H).serve_forever()

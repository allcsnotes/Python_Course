"""A tiny stand-in for the allcsvideos API: GET /courses from a CSV."""
import csv, json, sys
from http.server import BaseHTTPRequestHandler, HTTPServer

rows = [dict(id=int(r["id"]), title=r["title"], level=r["level"], price=int(r["price"]))
        for r in csv.DictReader(open(sys.argv[2]))]

class H(BaseHTTPRequestHandler):
    def do_GET(self):
        ok = self.path == "/courses"
        body = json.dumps(rows if ok else {"detail": "Not Found"}).encode()
        self.send_response(200 if ok else 404)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers(); self.wfile.write(body)
    def log_message(self, *a): pass

HTTPServer(("127.0.0.1", int(sys.argv[1])), H).serve_forever()

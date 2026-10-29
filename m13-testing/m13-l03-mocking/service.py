import json
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

COURSES = {
    "c101": {"id": "c101", "title": "Python Basics", "price": 500},
    "c102": {"id": "c102", "title": "SQL Basics", "price": 1000},
}


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        time.sleep(0.5)
        course = COURSES.get(self.path.rsplit("/", 1)[-1])
        body = json.dumps(course or {"error": "not found"}).encode()
        self.send_response(200 if course else 404)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *args):
        pass


ThreadingHTTPServer(("127.0.0.1", 8133), Handler).serve_forever()

import json
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

COURSES = [
    {"id": "C101", "title": "Python", "price": 499},
    {"id": "C102", "title": "SQL", "price": 399},
    {"id": "C103", "title": "Docker", "price": 449},
]


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/slow":
            time.sleep(3)
        if self.path in ("/courses", "/slow"):
            body = json.dumps(COURSES).encode()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
        elif self.path == "/oops":
            self.send_error(500)
        else:
            self.send_error(404)

    def log_message(self, *args):
        pass


ThreadingHTTPServer(("127.0.0.1", 8074), Handler).serve_forever()

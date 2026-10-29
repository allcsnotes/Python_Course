import json
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

TITLES = {1: "Python", 2: "SQL", 3: "Docker", 4: "Git",
          5: "Linux", 6: "Redis", 7: "Kafka", 8: "Spring Boot"}
DELAY = {1: 0.9, 2: 0.4, 3: 0.7, 4: 0.2,
         5: 0.6, 6: 1.0, 7: 0.3, 8: 0.8}


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        n = int(self.path.rsplit("/", 1)[-1])
        time.sleep(DELAY.get(n, 0.1))
        if n in TITLES:
            status, body = 200, {"id": n, "title": TITLES[n]}
        else:
            status, body = 404, {"error": "no such course"}
        data = json.dumps(body).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def log_message(self, *args):
        pass


ThreadingHTTPServer(("localhost", 8122), Handler).serve_forever()

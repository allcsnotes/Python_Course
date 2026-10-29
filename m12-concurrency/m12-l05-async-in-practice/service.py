import json
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

LIMIT = 20
lock = threading.Lock()
state = {"now": 0, "peak": 0, "busy": 0}


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *args):
        pass

    def send(self, code, body):
        data = json.dumps(body).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        path = self.path
        if path == "/stats":
            return self.send(200, state)
        if path == "/reset":
            state.update(peak=0, busy=0)
            return self.send(200, state)
        if path == "/missing":
            return self.send(404, {"error": "not found"})
        with lock:
            if state["now"] >= LIMIT:
                state["busy"] += 1
                return self.send(503, {"error": "busy"})
            state["now"] += 1
            state["peak"] = max(state["peak"], state["now"])
        try:
            wait = 5 if path == "/slow" else 0.5
            time.sleep(wait)
            n = path.rsplit("/", 1)[-1]
            self.send(200, {"page": n, "title": f"Course {n}"})
        finally:
            with lock:
                state["now"] -= 1


class Server(ThreadingHTTPServer):
    request_queue_size = 256
    daemon_threads = True


if __name__ == "__main__":
    Server(("127.0.0.1", 8125), Handler).serve_forever()

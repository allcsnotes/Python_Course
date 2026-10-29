import http.server
import threading
import time

LIMIT = 16
lock = threading.Lock()
state = {"now": 0, "peak": 0}


class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/_peak":
            return self.reply(200, str(state["peak"]))
        if self.path == "/_reset":
            state["peak"] = 0
            return self.reply(200, "reset")
        with lock:
            state["now"] += 1
            state["peak"] = max(state["peak"], state["now"])
            busy = state["now"] > LIMIT
        try:
            answer = (503, "too busy", None) if busy else self.route()
        finally:
            with lock:
                state["now"] -= 1
        self.reply(*answer)

    def route(self):
        kind, _, slug = self.path.strip("/").partition("/")
        if kind == "course":
            time.sleep(0.2)
            return 200, "course " + slug, None
        if kind == "video":
            time.sleep(1.0)
            return 200, "video " + slug, None
        if kind == "old":
            return 301, "", "/course/" + slug
        if kind == "api":
            return 500, "server error", None
        if kind == "hang":
            time.sleep(5)
            return 200, "too late", None
        return 404, "not found", None

    def reply(self, code, text, where=None):
        body = text.encode()
        self.send_response(code)
        if where:
            self.send_header("Location", where)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *args):
        pass


class Server(http.server.ThreadingHTTPServer):
    daemon_threads = True
    request_queue_size = 128


Server(("127.0.0.1", 8626), Handler).serve_forever()

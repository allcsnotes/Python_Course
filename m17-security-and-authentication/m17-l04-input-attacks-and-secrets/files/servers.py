import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

PAGES = {
    8174: {"/logo.png": "PNG-bytes-of-a-public-image"},
    8274: {"/admin/notes": "internal only: staff notes, never public"},
}


def handler_for(pages):
    class H(BaseHTTPRequestHandler):
        def do_GET(self):
            body = pages.get(self.path)
            self.send_response(200 if body else 404)
            self.end_headers()
            self.wfile.write((body or "not found").encode())

        def log_message(self, *a):
            pass

    return H


def start():
    for port, pages in PAGES.items():
        srv = HTTPServer(("127.0.0.1", port), handler_for(pages))
        threading.Thread(target=srv.serve_forever, daemon=True).start()

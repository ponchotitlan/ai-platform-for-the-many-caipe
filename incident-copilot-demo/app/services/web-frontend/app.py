"""web-frontend: serves the static page and forwards /api/pay to checkout-api."""
import os, urllib.error, urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

CHECKOUT_URL = os.environ.get("CHECKOUT_URL", "http://checkout-api:8080/pay")
PAGE = open(os.path.join(os.path.dirname(__file__), "index.html"), "rb").read()


class Handler(BaseHTTPRequestHandler):
    def _send(self, code, data, ctype="application/json"):
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        if self.path == "/healthz":
            return self._send(200, b'{"status":"ok"}')
        self._send(200, PAGE, "text/html; charset=utf-8")

    def do_POST(self):
        if self.path != "/api/pay":
            return self._send(404, b'{"error":"not_found"}')
        body = self.rfile.read(int(self.headers.get("Content-Length", 0)))
        req = urllib.request.Request(CHECKOUT_URL, body, {"Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=15) as r:
                self._send(r.status, r.read())
        except urllib.error.HTTPError as e:
            print(f"checkout-api returned {e.code}", flush=True)
            self._send(502, b'{"error":"checkout_failed"}')
        except OSError as e:
            print(f"checkout-api unreachable: {e}", flush=True)
            self._send(502, b'{"error":"checkout_unreachable"}')

    def log_message(self, *a):
        pass


ThreadingHTTPServer(("", 8080), Handler).serve_forever()

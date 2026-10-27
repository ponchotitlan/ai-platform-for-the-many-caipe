"""checkout-api: POST /pay creates a payment through payments-gateway.

Timeout and retries come from env, so a config-only deploy can break it
(v1.4.0 sets GATEWAY_TIMEOUT_MS=500 while the gateway answers in 2 to 4.5 s).
"""
import json, os, socket, threading, time, urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

VERSION = os.environ.get("APP_VERSION", "dev")
GATEWAY_URL = os.environ.get("GATEWAY_URL", "http://payments-gateway:8080/charge")
TIMEOUT_MS = int(os.environ.get("GATEWAY_TIMEOUT_MS", "5000"))
RETRIES = int(os.environ.get("GATEWAY_RETRIES", "2"))
DB_HOST, DB_PORT = os.environ.get("DB_HOST", "postgres"), int(os.environ.get("DB_PORT", "5432"))
WINDOW_S, LIVENESS_FAILS = 30, 10

lock = threading.Lock()
recent = []  # (timestamp, ok) of finished payments
ok_total = fail_total = 0  # since process start; resets on restart


def record(ok):
    global ok_total, fail_total
    with lock:
        now = time.time()
        recent.append((now, ok))
        recent[:] = [r for r in recent if now - r[0] < WINDOW_S]
        ok_total, fail_total = ok_total + ok, fail_total + (not ok)


def ready():
    with lock:
        now = time.time()
        window = [ok for t, ok in recent if now - t < WINDOW_S]
    try:
        socket.create_connection((DB_HOST, DB_PORT), timeout=1).close()
    except OSError:
        return False, "database unreachable"
    if len(window) >= 5 and window.count(False) / len(window) > 0.5:
        return False, "payment failure rate above 50%"
    return True, "ok"


def charge(body):
    for attempt in range(1, RETRIES + 2):
        req = urllib.request.Request(GATEWAY_URL, json.dumps(body).encode(), {"Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=TIMEOUT_MS / 1000) as r:
                return json.loads(r.read())
        except (TimeoutError, socket.timeout, OSError) as e:
            print(f"ERROR gateway timeout after {TIMEOUT_MS}ms (attempt {attempt}/{RETRIES + 1}): {e}", flush=True)
    return None


class Handler(BaseHTTPRequestHandler):
    def _send(self, code, body):
        data = json.dumps(body).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        if self.path == "/healthz":  # liveness: fails once most payments since start have failed
            ok = not (fail_total >= LIVENESS_FAILS and fail_total > ok_total)
            return self._send(200 if ok else 500, {"status": "ok" if ok else "stuck", "version": VERSION})
        if self.path == "/ready":
            ok, why = ready()
            return self._send(200 if ok else 503, {"ready": ok, "reason": why})
        self._send(200, {"service": "checkout-api", "version": VERSION})

    def do_POST(self):
        if self.path != "/pay":
            return self._send(404, {"error": "not_found"})
        body = json.loads(self.rfile.read(int(self.headers.get("Content-Length", 0))) or b"{}")
        result = charge(body)
        record(result is not None)
        if result is None:
            return self._send(504, {"error": "payment_gateway_timeout"})
        print(f"payment ok invoice={body.get('invoice_id')} charge={result['charge_id']}", flush=True)
        self._send(200, {"status": "paid", "charge_id": result["charge_id"]})

    def log_message(self, *a):
        pass


print(f"checkout-api {VERSION} starting: GATEWAY_TIMEOUT_MS={TIMEOUT_MS} GATEWAY_RETRIES={RETRIES}", flush=True)
ThreadingHTTPServer(("", 8080), Handler).serve_forever()

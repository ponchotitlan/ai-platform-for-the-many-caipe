"""Mock card-payment provider. Healthy; adds 2 to 4.5 s latency to most charges."""
import json, os, random, time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse, parse_qs

SLOW_RATIO = float(os.environ.get("GATEWAY_SLOW_RATIO", "0.9"))  # share of charges that are slow
MIN_S, MAX_S = 2.0, 4.5


class Handler(BaseHTTPRequestHandler):
    def _send(self, code, body):
        data = json.dumps(body).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        self._send(200, {"status": "ok", "service": "payments-gateway"})

    def do_POST(self):
        url = urlparse(self.path)
        n = int(self.headers.get("Content-Length", 0))
        charge = json.loads(self.rfile.read(n) or b"{}")
        forced = parse_qs(url.query).get("latency", ["auto"])[0]  # auto | none | slow
        slow = forced == "slow" or (forced == "auto" and random.random() < SLOW_RATIO)
        delay = random.uniform(MIN_S, MAX_S) if slow else 0.05
        time.sleep(delay)
        print(f"charge invoice={charge.get('invoice_id')} latency={delay:.2f}s approved", flush=True)
        self._send(200, {"approved": True, "charge_id": f"ch_{random.randrange(10**8):08d}", "latency_s": round(delay, 2)})

    def log_message(self, *a):
        pass


ThreadingHTTPServer(("", 8080), Handler).serve_forever()

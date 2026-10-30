"""Local stand-in for Splunk HEC used only to test the pipeline. Logs a summary of every batch."""
import json, sys
from http.server import BaseHTTPRequestHandler, HTTPServer
class H(BaseHTTPRequestHandler):
    def do_POST(self):
        b = self.rfile.read(int(self.headers.get("Content-Length", 0))); ok = self.headers.get("Authorization") == "Splunk test-token"
        rows = [l for l in b.decode(errors="replace").splitlines() if l.strip()]
        kinds = {}
        for r in rows:
            try: j = json.loads(r); k = j.get("sourcetype") or j.get("event", {}).get("metric_name", "?") if isinstance(j.get("event"), dict) else j.get("sourcetype", "?")
            except Exception: k = "?"
            kinds[k] = kinds.get(k, 0) + 1
        print(self.path, "auth_ok" if ok else "AUTH_FAIL", len(rows), "rows", dict(list(kinds.items())[:6]), flush=True)
        if rows: open("/tmp/last_batch.json", "wb").write(b)
        self.send_response(200 if ok else 403); self.end_headers(); self.wfile.write(b'{"text":"Success","code":0}')
    def log_message(self, *a): pass
HTTPServer(("0.0.0.0", 8088), H).serve_forever()

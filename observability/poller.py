"""Ships CAIPE usage metadata to Splunk HEC (events index).

Sources: Langfuse (traces + LLM generations: tokens, cost, latency) and MongoDB (conversation owner / team).
Only metadata is exported (no prompts, responses or tool arguments).
"""
import base64, hashlib, json, os, sys, time, urllib.request, urllib.parse
from pymongo import MongoClient

E = os.environ
HEC = E["SPLUNK_HEC_URL"].rstrip("/") + "/services/collector/event"
HEC_TOKEN = E["SPLUNK_HEC_TOKEN"]
INDEX = E.get("SPLUNK_EVENTS_INDEX", "caipe_events")
LF = E.get("LANGFUSE_HOST", "http://langfuse-web:3000").rstrip("/")
LF_AUTH = "Basic " + base64.b64encode(f"{E['LANGFUSE_PUBLIC_KEY']}:{E['LANGFUSE_SECRET_KEY']}".encode()).decode()
BACKFILL_DAYS = int(E.get("BACKFILL_DAYS", "30"))
INTERVAL = int(E.get("POLL_INTERVAL", "60"))
HASH_USERS = E.get("HASH_USER_IDS", "false").lower() == "true"
STATE = E.get("STATE_FILE", "/state/state.json")
CTX = None
if E.get("SPLUNK_HEC_INSECURE_SKIP_VERIFY", "false").lower() == "true":
    import ssl; CTX = ssl._create_unverified_context()

db = MongoClient(E["MONGODB_URI"], serverSelectionTimeoutMS=10000)[E.get("MONGODB_DATABASE", "caipe")]


def log(*a): print(time.strftime("%FT%T"), *a, flush=True)


def load_state():
    try: return json.load(open(STATE))
    except Exception: return {}


def save_state(s):
    os.makedirs(os.path.dirname(STATE), exist_ok=True)
    json.dump(s, open(STATE, "w"))


def lf_get(path, **params):
    url = f"{LF}/api/public/{path}?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"Authorization": LF_AUTH})
    return json.load(urllib.request.urlopen(req, timeout=30))


def lf_pages(path, **params):
    page = 1
    while True:
        d = lf_get(path, page=page, limit=100, **params)
        yield from d["data"]
        if page >= d["meta"]["totalPages"]: return
        page += 1


def user_id(email):
    if not email: return "unknown"
    return hashlib.sha256(email.encode()).hexdigest()[:16] if HASH_USERS else email


_owner_cache = {}
def owner_of(session_id):
    """Langfuse sessionId == CAIPE conversation _id."""
    if session_id in _owner_cache: return _owner_cache[session_id]
    c = db.conversations.find_one({"_id": session_id}, {"owner_id": 1, "client_type": 1}) or {}
    email = c.get("owner_id")
    teams = sorted({m["team_slug"] for m in db.team_membership_sources.find(
        {"user_email": email, "status": "active"}, {"team_slug": 1})}) if email else []
    r = {"user": user_id(email), "teams": teams or ["none"], "client_type": c.get("client_type")}
    _owner_cache[session_id] = r
    return r


def hec_send(events):
    for i in range(0, len(events), 200):
        body = "\n".join(json.dumps(e) for e in events[i:i + 200]).encode()
        req = urllib.request.Request(HEC, data=body, headers={"Authorization": f"Splunk {HEC_TOKEN}"})
        urllib.request.urlopen(req, timeout=30, context=CTX).read()


def ev(sourcetype, ts, body):
    return {"time": ts, "index": INDEX, "source": "caipe-poller", "sourcetype": sourcetype, "event": body}


def epoch(iso):
    from datetime import datetime
    return datetime.fromisoformat(iso.replace("Z", "+00:00")).timestamp()


def cycle(state):
    # Langfuse timestamps are ms; overlap by one cycle and dedupe on ids.
    # Langfuse's ClickHouse query 500s on epoch-0 bounds, so the first run backfills BACKFILL_DAYS.
    since = state.get("since") or time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(time.time() - BACKFILL_DAYS * 86400))
    seen = set(state.get("seen", []))
    out, newest = [], since
    for t in lf_pages("traces", fromTimestamp=since):
        if t["id"] in seen: continue
        o = owner_of(t.get("sessionId"))
        _trace_info[t["id"]] = (t.get("sessionId"), (t.get("name") or "").replace("_", " "))
        out.append(ev("caipe:trace", epoch(t["timestamp"]), {
            "trace_id": t["id"], "session_id": t.get("sessionId"), "agent": (t.get("name") or "").replace("_", " "),
            "latency_s": t.get("latency"), "cost_usd": t.get("totalCost"), **o}))
        newest = max(newest, t["timestamp"]); seen.add(t["id"])
    for g in lf_pages("observations", type="GENERATION", fromStartTime=since):
        if g["id"] in seen: continue
        u = g.get("usageDetails") or {}
        sid, agent = trace_info(g.get("traceId"))
        out.append(ev("caipe:llm_call", epoch(g["startTime"]), {
            "generation_id": g["id"], "trace_id": g.get("traceId"), "session_id": sid, "agent": agent, "model": g.get("model"),
            "input_tokens": u.get("input"), "output_tokens": u.get("output"), "total_tokens": u.get("total"),
            "cost_usd": g.get("calculatedTotalCost"), "latency_s": g.get("latency"), **owner_of(sid)}))
        newest = max(newest, g["startTime"]); seen.add(g["id"])
    if out: hec_send(out)
    # keep the dedupe set bounded
    return {"since": newest, "seen": list(seen)[-5000:]}, len(out)


_trace_info = {}
def trace_info(trace_id):
    """(sessionId, agent name) for a trace; filled from the traces pass, else fetched once."""
    if trace_id not in _trace_info:
        try:
            t = lf_get(f"traces/{trace_id}")
            _trace_info[trace_id] = (t.get("sessionId"), (t.get("name") or "").replace("_", " "))
        except Exception:
            _trace_info[trace_id] = (None, None)
    return _trace_info[trace_id]


def inventory():
    """Daily snapshot of configured agents / users / teams (names only) for the dashboard filters."""
    return [ev("caipe:inventory", time.time(), {
        "agents": [a.get("name") for a in db.dynamic_agents.find({}, {"name": 1})],
        "users": db.users.count_documents({}), "teams": [t["slug"] for t in db.teams.find({}, {"slug": 1})],
        "mcp_servers": db.mcp_servers.count_documents({})})]


if __name__ == "__main__":
    state, last_inv = load_state(), 0
    while True:
        try:
            state, n = cycle(state); save_state(state)
            if time.time() - last_inv > 86400: hec_send(inventory()); last_inv = time.time()
            log(f"sent {n} events")
        except Exception as e:
            log("cycle failed:", repr(e))
        if "--once" in sys.argv: break
        time.sleep(INTERVAL)

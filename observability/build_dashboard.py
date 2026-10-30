"""Generates caipe_dashboard.json (Splunk Dashboard Studio, absolute-free grid layout). Run: python3 build_dashboard.py"""
import json
M, EV = "caipe_metrics", "caipe_events"
T = "$global_time.earliest$", "$global_time.latest$"
TEAM = 'teams{}="$team$"'  # Splunk extracts JSON arrays as teams{}
ev = lambda st, rest: f'index={EV} sourcetype={st} {TEAM} | {rest}'
# Counter metrics: rate_sum over the span x span seconds = increase. $__span is not available, so use a fixed 1h/5m bin chosen by the time range.
def mrate(metric, by):
    """Counter increase per hour: rate_sum over 5m bins x 300s, summed to 1h."""
    return (f'| mstats rate_sum({metric}) AS r WHERE index={M} span=5m BY {by} '
            f'| eval n=r*300 | timechart span=1h sum(n) AS n BY {by}')

PANELS = [  # id, title, type, query, (x,y,w,h), options
 ("k_req", "Requests", "splunk.singlevalue", ev("caipe:trace", "stats count"), (0,70,200,110), {"majorColor": "#1A73E8"}),
 ("k_users", "Active users", "splunk.singlevalue", ev("caipe:trace", "stats dc(user) AS users"), (210,70,200,110), {}),
 ("k_spend", "Spend (USD)", "splunk.singlevalue", ev("caipe:llm_call", "stats sum(cost_usd) AS spend | eval spend=round(spend,2)"), (420,70,200,110), {"numberPrefix": "$"}),
 ("k_tok", "Tokens", "splunk.singlevalue", ev("caipe:llm_call", "stats sum(total_tokens) AS tokens"), (630,70,200,110), {"unitPosition": "after"}),
 ("k_p95", "p95 request latency (s)", "splunk.singlevalue", ev("caipe:trace", "stats perc95(latency_s) AS p95 | eval p95=round(p95,1)"), (840,70,200,110), {}),
 ("k_err", "Tool error rate (%)", "splunk.singlevalue",
  f'| mstats rate_sum(da_tool_calls_total) AS r WHERE index={M} span=5m BY status | eval n=r*300 | stats sum(n) AS tot sum(eval(if(status!="success",n,0))) AS bad | eval pct=round(100*bad/tot,2) | fields pct',
  (1050,70,200,110), {"numberSuffix": "%"}),

 ("h1", "Adoption", "markdown", None, (0,190,1250,30), {}),
 ("c_req_agent", "Requests by agent", "splunk.column", ev("caipe:trace", "timechart span=1h count BY agent"), (0,225,620,280), {"stackMode": "stacked"}),
 ("c_req_team", "Requests by team", "splunk.column", ev("caipe:trace", "mvexpand teams{} | rename teams{} AS teams | timechart span=1h count BY teams"), (630,225,620,280), {"stackMode": "stacked"}),
 ("t_users", "Usage by user", "splunk.table",
  ev("caipe:trace", "stats count AS requests dc(session_id) AS conversations sum(cost_usd) AS spend_usd latest(_time) AS last_seen BY user | eval spend_usd=round(spend_usd,2), last_seen=strftime(last_seen,\"%F %T\") | sort - requests"),
  (0,515,1250,240), {}),

 ("h2", "LLM usage and cost", "markdown", None, (0,765,1250,30), {}),
 ("c_tok_agent", "Tokens by agent", "splunk.column", ev("caipe:llm_call", "timechart span=1h sum(total_tokens) BY agent"), (0,800,620,280), {"stackMode": "stacked"}),
 ("c_cost_model", "Spend by model (USD)", "splunk.column", ev("caipe:llm_call", "timechart span=1h sum(cost_usd) BY model"), (630,800,620,280), {"stackMode": "stacked"}),
 ("t_cost_team", "Spend and tokens by team", "splunk.table",
  ev("caipe:llm_call", "mvexpand teams{} | rename teams{} AS teams | stats sum(input_tokens) AS input sum(output_tokens) AS output sum(cost_usd) AS spend_usd count AS llm_calls BY teams | eval spend_usd=round(spend_usd,2) | sort - spend_usd"),
  (0,1090,620,250), {}),
 ("t_outliers", "Costliest requests (loop-depth outliers)", "splunk.table",
  ev("caipe:llm_call", "stats count AS llm_calls sum(input_tokens) AS input sum(output_tokens) AS output sum(cost_usd) AS cost_usd latest(agent) AS agent latest(user) AS user BY trace_id | eval cost_usd=round(cost_usd,3) | sort - cost_usd | head 10"),
  (630,1090,620,250), {}),

 ("h3", "Performance", "markdown", None, (0,1350,1250,30), {}),
 ("l_lat", "Request latency p50 / p95 by agent (s)", "splunk.table",
  ev("caipe:trace", "stats median(latency_s) AS p50 perc95(latency_s) AS p95 count BY agent | eval p50=round(p50,1), p95=round(p95,1)"), (0,1385,620,260), {}),
 ("l_ttfr", "Avg time to first response (s)", "splunk.line",
  f'| mstats rate_sum(da_turn_time_to_first_response_seconds_sum) AS s rate_sum(da_turn_time_to_first_response_seconds_count) AS c WHERE index={M} span=1h BY agent_name | eval ttfr=round(s/c,2) | xyseries _time agent_name ttfr',
  (630,1385,620,260), {}),
 ("c_turns_status", "Turns by outcome", "splunk.column", mrate("da_turns_total", "status"), (0,1655,620,260), {"stackMode": "stacked"}),
 ("l_llm_lat", "Avg LLM call latency by model (s)", "splunk.line",
  f'| mstats rate_sum(da_llm_call_duration_seconds_sum) AS s rate_sum(da_llm_call_duration_seconds_count) AS c WHERE index={M} span=1h BY model_id | eval lat=round(s/c,2) | xyseries _time model_id lat',
  (630,1655,620,260), {}),

 ("h4", "Tools and MCP servers", "markdown", None, (0,1925,1250,30), {}),
 ("c_tool_calls", "Tool calls by tool", "splunk.bar",
  f'| mstats rate_sum(da_tool_calls_total) AS r WHERE index={M} span=5m BY tool_name | eval n=r*300 | stats sum(n) AS calls BY tool_name | eval calls=round(calls,0) | sort - calls | head 15',
  (0,1960,620,300), {}),
 ("t_tool_health", "Tool health (calls, error %, avg latency s)", "splunk.table",
  f'| mstats rate_sum(da_tool_calls_total) AS c rate_sum(da_tool_call_duration_seconds_sum) AS d WHERE index={M} span=5m BY tool_name status | eval n=c*300, dur=d*300 | stats sum(n) AS calls sum(dur) AS dur sum(eval(if(status!="success",n,0))) AS errors BY tool_name | eval calls=round(calls,0), error_pct=round(100*errors/calls,2), avg_latency_s=round(dur/calls,2) | table tool_name calls error_pct avg_latency_s | sort - calls',
  (630,1960,620,300), {}),
]

ds, viz, structure = {}, {}, []
for pid, title, typ, q, (x,y,w,h), opts in PANELS:
    if typ == "markdown":
        viz[pid] = {"type": "splunk.markdown", "options": {"markdown": f"## {title}", "fontSize": "large"}}
    else:
        ds[f"ds_{pid}"] = {"type": "ds.search", "name": title, "options": {"query": q, "queryParameters": {"earliest": "$global_time.earliest$", "latest": "$global_time.latest$"}}}
        viz[pid] = {"type": typ, "title": title, "dataSources": {"primary": f"ds_{pid}"}, "options": opts}
    structure.append({"item": pid, "type": "block", "position": {"x": x, "y": y, "w": w, "h": h}})

dash = {
 "title": "CAIPE Admin Overview",
 "description": "Usage, LLM spend, performance and tool health for the CAIPE platform. Metadata only.",
 "inputs": {
   "input_time": {"type": "input.timerange", "title": "Time range", "options": {"token": "global_time", "defaultValue": "-24h@h,now"}},
   "input_team": {"type": "input.dropdown", "title": "Team", "options": {"token": "team", "defaultValue": "*", "items": [
       {"label": "All", "value": "*"}, {"label": "support", "value": "support"}, {"label": "oncall", "value": "oncall"}, {"label": "owner", "value": "owner"}, {"label": "super-admins", "value": "super-admins"}]}},
 },
 "defaults": {"dataSources": {"ds.search": {"options": {"queryParameters": {"earliest": "$global_time.earliest$", "latest": "$global_time.latest$"}}}}},
 "visualizations": viz, "dataSources": ds,
 "layout": {"type": "absolute", "options": {"width": 1260, "height": 2280, "display": "auto"},
            "structure": structure, "globalInputs": ["input_time", "input_team"]},
}
json.dump(dash, open("caipe_dashboard.json", "w"), indent=2)
print("panels:", len(PANELS), "searches:", len(ds))

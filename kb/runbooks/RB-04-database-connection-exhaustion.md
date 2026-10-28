---
id: RB-04
title: Database connection exhaustion
kb: runbooks
owner: platform
updated: 2026-04-11
status: current
tags: [database, postgres, connections]
---
# Database connection exhaustion

## Symptoms

*RB-04 · Database connection exhaustion · updated 2026-04-11*
Slow checkout, errors such as `too many connections` or `connection refused` in service logs, and timeouts that grow with traffic. The symptoms look similar to a bad deploy or a provider problem.

## Checks (in order)

*RB-04 · Database connection exhaustion · updated 2026-04-11*
1. Count active connections in `postgres`: `SELECT count(*) FROM pg_stat_activity;`
2. Compare with the limit: `SHOW max_connections;`
3. Look for idle-in-transaction sessions: `SELECT state, count(*) FROM pg_stat_activity GROUP BY state;`
4. Check the `postgres` pod: status, restarts, memory.
5. Look for `too many connections` in `checkout-api` logs. If it is absent, the database is not the problem.

## Likely causes

*RB-04 · Database connection exhaustion · updated 2026-04-11*
A missing connection pool limit, a leak in a service, or a traffic spike. Connection counts close to `max_connections` confirm it.

## Safe actions

*RB-04 · Database connection exhaustion · updated 2026-04-11*
Read-only queries and log reads. Connection counts that are well below the limit mean this runbook does not apply, so go back to RB-01.

## Actions that need approval

*RB-04 · Database connection exhaustion · updated 2026-04-11*
Raising `max_connections`, restarting the database or terminating sessions.

## When to escalate

*RB-04 · Database connection exhaustion · updated 2026-04-11*
Connections are at the limit and customers cannot pay. See RB-07.

Past case: PM-01. Do not blame the database unless the counts support it.

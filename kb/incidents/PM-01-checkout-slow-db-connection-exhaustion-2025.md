---
id: PM-01
title: Checkout slow: database connection exhaustion (2025)
kb: incidents
owner: platform
updated: 2025-09-30
status: current
tags: [checkout, database, connections, 2025]
---
# Checkout slow: database connection exhaustion (2025)

## Summary

*PM-01 · Checkout slow: database connection exhaustion (2025) · updated 2025-09-30*
In September 2025, checkout was slow for about 40 minutes and some payments failed. Severity SEV2.

## What customers saw

*PM-01 · Checkout slow: database connection exhaustion (2025) · updated 2025-09-30*
Invoice payments took 10 to 20 seconds and sometimes ended with "something went wrong".

## Timeline

*PM-01 · Checkout slow: database connection exhaustion (2025) · updated 2025-09-30*
- 14:05 Alerts: checkout latency above threshold.
- 14:12 On call checked recent deploys. None in the last 24 hours.
- 14:20 `pg_stat_activity` showed the database at its connection limit.
- 14:35 Idle sessions were terminated (approved by the owner). Latency recovered.
- 14:45 Resolved.

## Root cause

*PM-01 · Checkout slow: database connection exhaustion (2025) · updated 2025-09-30*
`checkout-api` opened a new database connection per request and had no connection pool limit. A traffic spike from an end-of-month invoice run used all available connections.

## What we checked and ruled out

*PM-01 · Checkout slow: database connection exhaustion (2025) · updated 2025-09-30*
The payment provider was healthy. No deploy had happened.

## What we changed

*PM-01 · Checkout slow: database connection exhaustion (2025) · updated 2025-09-30*
A connection pool limit in `checkout-api` and an alert on connection count above 80% of the limit.

## Lessons

*PM-01 · Checkout slow: database connection exhaustion (2025) · updated 2025-09-30*
The surface symptoms (slow checkout) look the same as a deploy or provider problem. Connection counts decide it: here they were at the limit. If they are normal, this incident does not apply. See RB-04.

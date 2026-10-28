---
id: PM-06
title: False-positive latency alert (2025)
kb: incidents
owner: platform
updated: 2025-12-02
status: current
tags: [alert, latency, false-positive, 2025]
---
# False-positive latency alert (2025)

## Summary

*PM-06 · False-positive latency alert (2025) · updated 2025-12-02*
In December 2025 a latency alert paged on call at night. After 30 minutes of investigation there was no customer impact. Severity SEV4.

## What happened

*PM-06 · False-positive latency alert (2025) · updated 2025-12-02*
The alert fired because a monitoring probe was routed through a slow network path. Real customer traffic was normal.

## Timeline

*PM-06 · False-positive latency alert (2025) · updated 2025-12-02*
- 02:10 Alert: checkout latency high.
- 02:15 On call opened an incident and prepared a rollback.
- 02:40 Real payment success rate was checked: normal. The alert came from the probe only.

## Root cause

*PM-06 · False-positive latency alert (2025) · updated 2025-12-02*
A synthetic probe moved to another network path, and its latency was not representative.

## What we changed

*PM-06 · False-positive latency alert (2025) · updated 2025-12-02*
The alert now needs both probe latency and a drop in real payment success rate.

## Lessons

*PM-06 · False-positive latency alert (2025) · updated 2025-12-02*
Verify the impact with a second signal (payment success rate, error logs, restarts) before escalating or changing production. A single alert is not an incident.

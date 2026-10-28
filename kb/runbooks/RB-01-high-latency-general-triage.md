---
id: RB-01
title: High latency, general triage
kb: runbooks
owner: platform
updated: 2026-05-20
status: current
tags: [latency, triage]
---
# High latency, general triage

## Symptoms

*RB-01 · High latency, general triage · updated 2026-05-20*
Users report slow pages or spinning buttons. Dashboards show higher response times on one or more LedgerLite services. No single cause is known yet.

## Checks (in order)

*RB-01 · High latency, general triage · updated 2026-05-20*
1. Confirm the report: reproduce it in the LedgerLite web app, and note the time it started.
2. List pods in the `ledgerlite` namespace: look at READY, STATUS and RESTARTS.
3. Check recent events for probe failures, OOM kills or scheduling problems.
4. Check what changed in the last day: deployments, config, traffic.
5. Compare the slow path with a healthy one (for example, browsing invoices versus paying one).

## Likely causes

*RB-01 · High latency, general triage · updated 2026-05-20*
A recent deploy, a dependency slowdown (database or payment provider), resource pressure, or a traffic spike.

## Safe actions

*RB-01 · High latency, general triage · updated 2026-05-20*
Read-only inspection: pod status, logs, events, rollout history. Write down what you see before changing anything.

## Actions that need approval

*RB-01 · High latency, general triage · updated 2026-05-20*
Any restart, scale, rollback or configuration change.

## When to escalate

*RB-01 · High latency, general triage · updated 2026-05-20*
Customers cannot complete payments for more than 10 minutes, or the cause is unclear after the checks above. See RB-07 for severity levels.

This runbook is generic. Once the slow service is known, move to the specific runbook: RB-02 for checkout after a deploy, RB-04 for database connections, RB-05 for payment provider problems.

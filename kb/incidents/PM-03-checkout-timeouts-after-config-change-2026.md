---
id: PM-03
title: Checkout timeouts after a config change (2026)
kb: incidents
owner: platform
updated: 2026-03-27
status: current
tags: [checkout, timeout, config, deploy, retries, 2026]
---
# Checkout timeouts after a config change (2026)

## Summary
In March 2026 payments failed for about 50 minutes after a `checkout-api` release lowered the payment gateway timeout. Severity SEV2.

## What customers saw
Paying an invoice spun and then showed "something went wrong". Most payments failed. A few customers retried and were charged twice.

## Timeline
- 10:02 Release 1.4.0 of `checkout-api` rolled out.
- 10:20 Payment failures rose. Readiness probes failed intermittently.
- 10:28 On call saw restarts and `Readiness probe failed` events. Logs showed `gateway timeout after 500ms`.
- 10:31 A pod restart was tried, following the restart-first guidance. Failures continued, and the restart made the retry load worse.
- 10:40 Rollout history showed revision 2 had changed `GATEWAY_TIMEOUT_MS` from 5000 to 500.
- 10:48 The deployment was rolled back to revision 1 (approved by the owner). Payments recovered.

## Root cause
`GATEWAY_TIMEOUT_MS` was changed from 5000 to 500 in release 1.4.0. The payment gateway normally answers in 2 to 5 seconds, so most calls timed out. Each failed call was retried (`GATEWAY_RETRIES=2`), which tripled the load on the gateway and made readiness checks fail.

## What we checked and ruled out
Database connections were normal. The gateway was healthy and its latency was unchanged. It was not a provider outage.

## What did not help
**Restarting the pod during timeouts made things worse.** Each restart dropped in-flight requests, clients retried, and the retry storm grew. Do not restart as a first step when the logs show gateway timeouts after a recent deploy.

## Fix
Roll back to the previous revision, or restore the timeout to 5000 ms. Add a review step for timeout changes.

## Lessons
Compare the current and previous revision first. A recent config change plus timeout log lines is enough to act on. See RB-02 and RB-03.

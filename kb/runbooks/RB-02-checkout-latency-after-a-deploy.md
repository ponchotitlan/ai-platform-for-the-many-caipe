---
id: RB-02
title: Checkout latency after a deploy
kb: runbooks
owner: platform
updated: 2026-08-14
status: current
tags: [checkout, latency, deploy, timeout]
---
# Checkout latency after a deploy

## Symptoms
Payments fail or take a long time shortly after a `checkout-api` release. Customers see "something went wrong". The pod may show restarts and `Readiness probe failed` events. Logs contain lines such as `gateway timeout after 500ms`.

## Checks (in order)
1. List the pods in `ledgerlite` and note the `checkout-api` RESTARTS and READY columns.
2. Read the events for `checkout-api`: probe failures and `Killing` events point to failing health checks.
3. Read the current logs, and the previous container's logs after a restart. Look for gateway timeouts and retry messages.
4. Check the rollout history. List the ReplicaSets of `checkout-api` and note when the current revision was created.
5. Compare the current revision with the previous one: image tag, environment variables (`GATEWAY_TIMEOUT_MS`, `GATEWAY_RETRIES`) and the `deploy.ledgerlite/change` annotation.
6. Check that the payments gateway itself is healthy (see RB-05) and that database connection counts are normal (see RB-04). If both are fine, the deploy is the cause.

## Likely causes
A timeout or retry value was lowered or raised in the last release. The payment gateway normally answers in 2 to 5 seconds, so a timeout below that makes most payments fail, and retries multiply the load.

## Safe actions
Read-only checks above. Draft an issue with the evidence (see RB-07).

## Actions that need approval
Rolling back to the previous revision (procedure in RB-03), or restoring the previous timeout value. Both change production and need human approval.

## When to escalate
Payments are failing for all customers, or the rollback does not restore normal behaviour within 10 minutes.

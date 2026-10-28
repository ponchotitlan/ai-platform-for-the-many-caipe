---
id: RB-05
title: Payment provider timeouts
kb: runbooks
owner: platform
updated: 2026-03-18
status: current
tags: [payments, provider, gateway]
---
# Payment provider timeouts

## Symptoms
Payments fail with timeouts or `502` responses. The cause may be on the provider side, in the `payments-gateway` service that fronts it, or in our own timeout settings.

## Checks (in order)
1. Check the `payments-gateway` pod: is it Ready, has it restarted?
2. Read its logs for upstream errors and latency figures.
3. Check the provider status page and any provider incident notices.
4. Measure gateway latency from inside the cluster. In the LedgerLite demo the gateway answers in about 2 to 5 seconds when healthy.
5. Compare that latency with the timeout configured in `checkout-api` (`GATEWAY_TIMEOUT_MS`). A timeout shorter than normal gateway latency causes failures even when the provider is healthy.

## Likely causes
A real provider outage (the provider status page confirms it), gateway overload, or a client timeout that is too short.

## Safe actions
Read-only checks. Do not declare a provider outage until the provider's own status and the gateway logs agree.

## Actions that need approval
Switching payment providers, scaling the gateway, or changing timeouts.

## When to escalate
Provider confirms an outage: raise severity per RB-07 and use the customer wording in RB-08.

Past case: PM-02.

---
id: PM-02
title: Payment failures: provider outage (2025)
kb: incidents
owner: payments
updated: 2025-06-18
status: current
tags: [payments, provider, outage, 2025]
---
# Payment failures: provider outage (2025)

## Summary
In June 2025 card payments failed for about 55 minutes because our payment provider had an outage. Severity SEV1.

## What customers saw
Card payments returned an error. Invoice browsing worked.

## Timeline
- 09:10 Payment error rate rose from under 1% to over 60%.
- 09:15 No deploy had happened. `payments-gateway` logs showed upstream `503` responses from the provider.
- 09:20 The provider's status page confirmed an incident.
- 09:25 Customer message sent using the approved wording (RB-08).
- 10:05 Provider recovered. Error rate returned to normal.

## Root cause
Provider-side outage. Nothing in our services had changed.

## What we checked and ruled out
No deploy, no database problem, no resource pressure on our pods.

## What we changed
We added the provider status feed to the on-call dashboard, and a check in RB-05 to read the provider status before anything else.

## Lessons
When the provider status page and the gateway logs both show upstream failures, it is an outage and our services need no changes. If the gateway is healthy and latency is normal, it is not a provider outage. See RB-05.

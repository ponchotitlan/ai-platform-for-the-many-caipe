---
id: RB-07
title: Severity levels and escalation
kb: runbooks
owner: incident-management
updated: 2026-07-01
status: current
tags: [severity, escalation, ticket]
---
# Severity levels and escalation

## Symptoms
An incident needs a severity, an owner and a ticket.

## Checks (in order)
1. How many customers are affected: one, some, or all?
2. Is a core flow broken (paying an invoice), or only a side feature?
3. Is there a workaround?
4. Is revenue or customer data at risk?

## Severity levels
- **SEV1**: all customers cannot pay, or data is at risk. Page the on-call engineer and the platform owner. Update every 15 minutes.
- **SEV2**: many customers affected, or a core flow is degraded with no workaround. Page on call. Update every 30 minutes.
- **SEV3**: limited impact or a workaround exists. Handle in working hours.
- **SEV4**: cosmetic or no customer impact.

## Owners
The platform team owns LedgerLite services (`web-frontend`, `checkout-api`, `payments-gateway`, `postgres`). The payments lead owns provider relations.

## Ticket contents
A good issue has: a title with the severity and service, the symptoms with timestamps, the evidence (log lines, events, revisions), what was checked and ruled out, the suggested fix, and the owner.

## Actions that need approval
Creating the issue in the tracker needs approval in this environment. The copilot drafts it and shows the title and body to a person first.

## When to escalate
Raise severity when impact grows or the fix is not working after 30 minutes.

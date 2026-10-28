---
id: RB-03
title: Bad deploy: rollback procedure
kb: runbooks
owner: platform
updated: 2026-06-02
status: current
tags: [rollback, deploy, approval]
---
# Bad deploy: rollback procedure

## Symptoms

*RB-03 · Bad deploy: rollback procedure · updated 2026-06-02*
A release caused errors or latency, the cause is a change in the new revision, and the previous revision was healthy.

## Checks (in order)

*RB-03 · Bad deploy: rollback procedure · updated 2026-06-02*
1. Confirm the previous revision was healthy: look at the rollout history and any incident notes.
2. Confirm that the problem started after the new revision rolled out, not before.
3. Identify the exact change between revisions (image tag, environment variables, annotations).
4. Check that rolling back does not undo a required database or schema change.

## Likely causes

*RB-03 · Bad deploy: rollback procedure · updated 2026-06-02*
A configuration change or code change in the latest release.

## Safe actions

*RB-03 · Bad deploy: rollback procedure · updated 2026-06-02*
Inspect only. Prepare the rollback command and the expected result so the approver can read them.

## Actions that need approval

*RB-03 · Bad deploy: rollback procedure · updated 2026-06-02*
The rollback itself. Every step below changes production and requires explicit human approval, on call or owner:
1. `kubectl -n ledgerlite rollout history deployment/checkout-api`
2. `kubectl -n ledgerlite rollout undo deployment/checkout-api`
3. `kubectl -n ledgerlite rollout status deployment/checkout-api`
4. Confirm that pods are Ready, restarts stop, and payments succeed again.

The commands are written for people. The incident copilot has read-only access and never runs them. It proposes the rollback and waits for a person.

## When to escalate

*RB-03 · Bad deploy: rollback procedure · updated 2026-06-02*
The rollback fails, the previous revision is also unhealthy, or customer payments stay broken after 10 minutes. Raise severity per RB-07.

---
id: RB-06
title: Pod restart first aid
kb: runbooks
owner: platform
updated: 2024-02-12
status: current
tags: [restart, pod, first-aid]
---
# Pod restart first aid

## Symptoms

*RB-06 · Pod restart first aid · updated 2024-02-12*
A pod is slow, stuck or failing health checks, and nobody knows why yet.

## Checks (in order)

*RB-06 · Pod restart first aid · updated 2024-02-12*
1. Note the pod name, its RESTARTS count and its age.
2. Capture the logs before restarting. A restart loses the evidence.
3. Check the events for the pod.

## Likely causes

*RB-06 · Pod restart first aid · updated 2024-02-12*
Memory leaks, stuck workers, or a bad dependency.

## Safe actions

*RB-06 · Pod restart first aid · updated 2024-02-12*
Capture logs and events.

## Actions that need approval

*RB-06 · Pod restart first aid · updated 2024-02-12*
**Restart the pod first.** In most cases a restart clears the problem within a minute: delete the pod and let the Deployment replace it (`kubectl -n ledgerlite delete pod <name>`). Check that the new pod becomes Ready. If the problem comes back, continue with the specific runbook for the service.

## When to escalate

*RB-06 · Pod restart first aid · updated 2024-02-12*
The problem returns after two restarts. See RB-07.

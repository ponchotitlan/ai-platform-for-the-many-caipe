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
A pod is slow, stuck or failing health checks, and nobody knows why yet.

## Checks (in order)
1. Note the pod name, its RESTARTS count and its age.
2. Capture the logs before restarting. A restart loses the evidence.
3. Check the events for the pod.

## Likely causes
Memory leaks, stuck workers, or a bad dependency.

## Safe actions
Capture logs and events.

## Actions that need approval
**Restart the pod first.** In most cases a restart clears the problem within a minute: delete the pod and let the Deployment replace it (`kubectl -n ledgerlite delete pod <name>`). Check that the new pod becomes Ready. If the problem comes back, continue with the specific runbook for the service.

## When to escalate
The problem returns after two restarts. See RB-07.

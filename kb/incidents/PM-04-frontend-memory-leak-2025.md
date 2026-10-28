---
id: PM-04
title: Frontend memory leak (2025)
kb: incidents
owner: platform
updated: 2025-03-14
status: current
tags: [frontend, memory, 2025]
---
# Frontend memory leak (2025)

## Summary
In March 2025 the `web-frontend` pod was killed repeatedly for exceeding its memory limit. Severity SEV3.

## What customers saw
The invoice page occasionally failed to load for a few seconds, then recovered.

## Timeline
- 11:00 `OOMKilled` events for `web-frontend`.
- 11:30 Memory use grew steadily between restarts.
- 13:00 A fix released: an in-memory cache of invoice pages was given a size limit.

## Root cause
An unbounded in-memory cache in the frontend.

## What we checked and ruled out
Payments were not affected. Checkout and the database were healthy.

## Lessons
Check pod events for `OOMKilled` and memory growth. This incident is unrelated to payment failures.

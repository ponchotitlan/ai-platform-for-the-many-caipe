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

*PM-04 · Frontend memory leak (2025) · updated 2025-03-14*
In March 2025 the `web-frontend` pod was killed repeatedly for exceeding its memory limit. Severity SEV3.

## What customers saw

*PM-04 · Frontend memory leak (2025) · updated 2025-03-14*
The invoice page occasionally failed to load for a few seconds, then recovered.

## Timeline

*PM-04 · Frontend memory leak (2025) · updated 2025-03-14*
- 11:00 `OOMKilled` events for `web-frontend`.
- 11:30 Memory use grew steadily between restarts.
- 13:00 A fix released: an in-memory cache of invoice pages was given a size limit.

## Root cause

*PM-04 · Frontend memory leak (2025) · updated 2025-03-14*
An unbounded in-memory cache in the frontend.

## What we checked and ruled out

*PM-04 · Frontend memory leak (2025) · updated 2025-03-14*
Payments were not affected. Checkout and the database were healthy.

## Lessons

*PM-04 · Frontend memory leak (2025) · updated 2025-03-14*
Check pod events for `OOMKilled` and memory growth. This incident is unrelated to payment failures.

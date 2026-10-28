---
id: PM-05
title: Expired TLS certificate (2024)
kb: incidents
owner: security
updated: 2024-11-05
status: current
tags: [tls, certificate, 2024]
---
# Expired TLS certificate (2024)

## Summary
In November 2024 the public certificate for the LedgerLite web address expired. Severity SEV2 for 25 minutes.

## What customers saw
Browsers showed a security warning and refused to load the app.

## Timeline
- 08:00 Customers reported certificate warnings.
- 08:10 The certificate was confirmed expired.
- 08:25 A renewed certificate was installed.

## Root cause
The automatic renewal job had been failing silently for 30 days.

## What we changed
An alert 21 days before expiry and a monthly check of the renewal job.

## Lessons
Certificate errors appear in the browser, not in service logs. This incident is unrelated to slow or failing payments inside the app.

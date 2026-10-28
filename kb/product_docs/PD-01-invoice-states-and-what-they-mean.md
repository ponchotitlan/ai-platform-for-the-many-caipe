---
id: PD-01
title: Invoice states and what they mean
kb: product_docs
owner: product
updated: 2026-05-05
status: current
tags: [invoices, states]
---
# Invoice states and what they mean

## Overview
Every LedgerLite invoice has a state that tells you where it is in its life. This page explains each state in plain language.

## States
- **Draft**: the invoice is being prepared and has not been sent.
- **Open**: the invoice has been sent and is waiting for payment.
- **Processing**: a card payment has been started and is waiting for confirmation. This usually takes a few seconds.
- **Paid**: the payment was confirmed. A receipt is available.
- **Failed**: the last payment attempt did not go through. The invoice stays open for another try.
- **Void**: the invoice was cancelled and no longer needs payment.

## Things to know
- An invoice in **Processing** for more than a few minutes should be checked before another attempt is made, to avoid paying twice.
- A **Failed** payment does not charge the card. If you see a charge on your statement for a failed payment, see the page on duplicate charges.
- Only the account owner can void an invoice.

## Getting help
If an invoice shows a state that does not match what you expect, contact support with the invoice number.

#!/usr/bin/env bash
# Restore the broken state: v1.3.2 (healthy) becomes revision 1, v1.4.0 (timeout 500 ms) revision 2.
set -euo pipefail
source "$(dirname "$0")/lib.sh"
kubectl -n "$NS" delete deploy/checkout-api --ignore-not-found --wait=true
kubectl apply -f "$K8S/checkout-api.v1.3.2.yaml"
kubectl -n "$NS" rollout status deploy/checkout-api --timeout=60s
kubectl apply -f "$K8S/checkout-api.v1.4.0.yaml"
kubectl -n "$NS" rollout status deploy/checkout-api --timeout=60s || true  # may flap on purpose
echo "Fault planted: checkout-api v1.4.0, GATEWAY_TIMEOUT_MS=500."

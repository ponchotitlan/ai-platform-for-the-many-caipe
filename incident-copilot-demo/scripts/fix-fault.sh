#!/usr/bin/env bash
# For the human to run: roll checkout-api back to v1.3.2 (timeout 5000 ms). Agents never do this.
set -euo pipefail
source "$(dirname "$0")/lib.sh"
kubectl -n "$NS" rollout undo deploy/checkout-api --to-revision=1
kubectl -n "$NS" rollout status deploy/checkout-api --timeout=60s
echo "Fixed: checkout-api is back on v1.3.2."

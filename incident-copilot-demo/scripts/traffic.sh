#!/usr/bin/env bash
# Generate payment requests so logs, restarts and probe failures look alive. Ctrl-C to stop.
# Usage: scripts/traffic.sh [workers=2] [pause_seconds=1]
set -uo pipefail
source "$(dirname "$0")/lib.sh"
WORKERS="${1:-2}"; PAUSE="${2:-1}"
trap 'kill 0' INT TERM
worker() {
  while true; do
    code=$(curl -s -o /dev/null -m 20 -w '%{http_code}' -X POST "$FRONTEND_URL/api/pay" \
      -H 'Content-Type: application/json' -d '{"invoice_id":"INV-1007","amount_cents":13425}')
    echo "$(date +%T) worker=$1 /api/pay -> $code"
    sleep "$PAUSE"
  done
}
for i in $(seq "$WORKERS"); do worker "$i" & done
wait

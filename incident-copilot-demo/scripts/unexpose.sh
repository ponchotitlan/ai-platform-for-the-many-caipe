#!/usr/bin/env bash
# Recreate cloudflared with only the CAIPE compose files (detaches it from the kind network).
set -euo pipefail
CAIPE_DIR="${CAIPE_DIR:-/home/ubuntu/ai-platform-engineering}"
cd "$CAIPE_DIR"
docker compose -f docker-compose.yaml -f docker-compose.override.yaml up -d --no-deps --force-recreate cloudflared

#!/usr/bin/env bash
# Attach the CAIPE cloudflared container to the kind network (recreates only that container).
# CAIPE_DIR defaults to the install path; override with CAIPE_DIR=/path.
set -euo pipefail
source "$(dirname "$0")/lib.sh"
CAIPE_DIR="${CAIPE_DIR:-/home/ubuntu/ai-platform-engineering}"
docker network inspect kind >/dev/null  # fail early: a missing network would keep cloudflared from starting
cd "$CAIPE_DIR"
docker compose -f docker-compose.yaml -f docker-compose.override.yaml \
  -f "$ROOT/compose/docker-compose.cloudflared-kind.yaml" up -d --no-deps cloudflared

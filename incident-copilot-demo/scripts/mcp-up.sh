#!/usr/bin/env bash
# Start the read-only Kubernetes MCP server inside CAIPE's compose project.
set -euo pipefail
source "$(dirname "$0")/lib.sh"
CAIPE_DIR="${CAIPE_DIR:-/home/ubuntu/ai-platform-engineering}"
"$ROOT/scripts/agent-kubeconfig.sh"
export DEMO_UID="$(id -u)" DEMO_GID="$(id -g)"
export DEMO_KUBECONFIG="$ROOT/.kube/agent-readonly.kubeconfig"
cd "$CAIPE_DIR"
docker compose -f docker-compose.yaml -f docker-compose.override.yaml \
  -f "$ROOT/compose/docker-compose.k8s-mcp.yaml" up -d --no-deps --force-recreate k8s-readonly-mcp
echo "MCP endpoint inside CAIPE's network: http://k8s-readonly-mcp:8000/mcp"

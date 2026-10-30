#!/usr/bin/env bash
# Stop and remove the write-enabled Kubernetes MCP server container.
set -euo pipefail
docker rm -f k8s-ops-mcp

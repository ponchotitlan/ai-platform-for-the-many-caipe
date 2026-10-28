#!/usr/bin/env bash
# Stop and remove the read-only Kubernetes MCP server container.
set -euo pipefail
docker rm -f k8s-readonly-mcp

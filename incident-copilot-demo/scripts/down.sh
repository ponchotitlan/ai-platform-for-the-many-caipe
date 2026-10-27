#!/usr/bin/env bash
# Delete the kind cluster and its kubeconfig.
set -euo pipefail
source "$(dirname "$0")/lib.sh"
kind delete cluster --name "$CLUSTER"
rm -f "$KUBECONFIG"

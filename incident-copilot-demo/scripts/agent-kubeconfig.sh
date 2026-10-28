#!/usr/bin/env bash
# Apply the read-only RBAC and write .kube/agent-readonly.kubeconfig for the MCP server.
# The server address is the kind node's name on the `kind` Docker network, so a container on that network can use it.
set -euo pipefail
source "$(dirname "$0")/lib.sh"

kubectl apply -f "$K8S/rbac-agent-readonly.yaml" >/dev/null
for _ in $(seq 1 30); do
  TOKEN=$(kubectl -n "$NS" get secret copilot-readonly-token -o jsonpath='{.data.token}' | base64 -d)
  [ -n "$TOKEN" ] && break
  sleep 1
done
CA=$(kubectl -n "$NS" get secret copilot-readonly-token -o jsonpath='{.data.ca\.crt}')

OUT="$ROOT/.kube/agent-readonly.kubeconfig"
cat > "$OUT" <<KC
apiVersion: v1
kind: Config
clusters:
  - name: $CLUSTER
    cluster:
      server: https://$CLUSTER-control-plane:6443
      certificate-authority-data: $CA
users:
  - name: copilot-readonly
    user:
      token: $TOKEN
contexts:
  - name: copilot
    context: {cluster: $CLUSTER, user: copilot-readonly, namespace: $NS}
current-context: copilot
KC
chmod 600 "$OUT"
echo "wrote $OUT"

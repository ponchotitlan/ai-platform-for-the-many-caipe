# Shared settings for the LedgerLite scripts. Source it, do not run it.
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CLUSTER=ledgerlite
NS=ledgerlite
export KUBECONFIG="$ROOT/.kube/kind-$CLUSTER"
K8S="$ROOT/app/k8s"
SVC="$ROOT/app/services"
FRONTEND_URL="http://127.0.0.1:8088"

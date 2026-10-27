#!/usr/bin/env bash
# Create the kind cluster, build and load the LedgerLite images, deploy, then plant the fault.
set -euo pipefail
source "$(dirname "$0")/lib.sh"
mkdir -p "$ROOT/.kube"

if ! kind get clusters 2>/dev/null | grep -qx "$CLUSTER"; then
  kind create cluster --name "$CLUSTER" --config "$K8S/kind-config.yaml" --kubeconfig "$KUBECONFIG"
else
  kind export kubeconfig --name "$CLUSTER" --kubeconfig "$KUBECONFIG"
fi
chmod 600 "$KUBECONFIG"

build() { docker build -q -t "ledgerlite/$1:$2" --build-arg "APP_VERSION=$2" "$SVC/$1" >/dev/null; echo "built ledgerlite/$1:$2"; }
build payments-gateway v2.0.1
build web-frontend v3.3.0
build checkout-api v1.3.2
build checkout-api v1.4.0
kind load docker-image --name "$CLUSTER" \
  ledgerlite/payments-gateway:v2.0.1 ledgerlite/web-frontend:v3.3.0 \
  ledgerlite/checkout-api:v1.3.2 ledgerlite/checkout-api:v1.4.0

kubectl apply -f "$K8S/00-namespace.yaml"
kubectl apply -f "$K8S/postgres.yaml" -f "$K8S/payments-gateway.yaml" -f "$K8S/web-frontend.yaml" -f "$K8S/checkout-api.service.yaml"
kubectl -n "$NS" rollout status deploy/postgres deploy/payments-gateway deploy/web-frontend --timeout=120s

"$ROOT/scripts/reset-fault.sh"
echo "LedgerLite is up at $FRONTEND_URL (checkout-api v1.4.0 is broken on purpose)."

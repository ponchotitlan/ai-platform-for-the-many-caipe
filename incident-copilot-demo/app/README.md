# LedgerLite (sample app)

Fictional invoicing and card-payments product on a local kind cluster. It exists to fail in one repeatable way. See `docs/SPEC.md` section 3.

| Service | Image | Notes |
| --- | --- | --- |
| web-frontend | `ledgerlite/web-frontend:v3.3.0` | Page at http://127.0.0.1:8088, forwards `/api/pay` to checkout-api |
| checkout-api | `ledgerlite/checkout-api:v1.3.2` / `v1.4.0` | Same code; the deploy manifest decides `GATEWAY_TIMEOUT_MS` (5000 vs 500) |
| payments-gateway | `ledgerlite/payments-gateway:v2.0.1` | Mock provider, 2 to 4.5 s latency on 90% of charges |
| postgres | `postgres:16-alpine` | 5 customers, 20 synthetic invoices |

All services are stdlib-only Python (`app/services/`), manifests are in `k8s/`.

## Scripts (`incident-copilot-demo/scripts/`, next to this folder)

- `up.sh`: create the cluster (kubeconfig at `.kube/kind-ledgerlite`, git-ignored), build and load images, deploy, plant the fault
- `reset-fault.sh`: delete and redeploy checkout-api as revision 1 (v1.3.2) then revision 2 (v1.4.0, broken). About 5 s.
- `fix-fault.sh`: for the human only; `rollout undo` to revision 1
- `traffic.sh [workers] [pause]`: keep requests flowing so restarts and probe failures appear (about 1 to 2 minutes after the first request)
- `down.sh`: delete the cluster

From `incident-copilot-demo/`: `export KUBECONFIG=$PWD/.kube/kind-ledgerlite`.

## The fault

checkout-api v1.4.0 sets `GATEWAY_TIMEOUT_MS=500`. Rollout revision 2 carries the annotation `deploy.ledgerlite/change: "timeout 5000->500"`. Symptoms: payments return 502 on the page, `ERROR gateway timeout after 500ms` log lines, `Readiness probe failed` events, restarts above 0. Postgres and the gateway stay healthy.

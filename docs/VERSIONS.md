# Pinned versions

Recorded in Phase 0 on 2026-10-26 from the running install. Do not change without updating this file.

## CAIPE install (Docker Compose)

- Install path: `/home/ubuntu/ai-platform-engineering` (untouched by this repo)
- Source: git `12e9b495d`, tag `1.3.0-rc.16`
- Compose project: `ai-platform-engineering`
- Compose files: `docker-compose.yaml` + the user's existing `docker-compose.override.yaml` (MinIO image swap, Langfuse on 3100, Cloudflare tunnel, Keycloak hostname)
- Profiles (`.env`): `caipe-ui-prod,rbac,dynamic-agents,rag,caipe-mongodb,web_ingestor,tracing`
- `IMAGE_TAG` is unset in `.env`, so compose falls back to `0.5.66`. The images run 0.5.66 while the source is 1.3.0-rc.16. Treat 0.5.66 as the version of record.

## Running images

| Service | Image |
| --- | --- |
| caipe-ui | ghcr.io/cnoe-io/caipe-ui:0.5.66 |
| dynamic-agents | ghcr.io/cnoe-io/caipe-dynamic-agents:0.5.66 |
| rag-server | ghcr.io/cnoe-io/caipe-rag-server:0.5.66 |
| web-ingestor | ghcr.io/cnoe-io/caipe-rag-ingestors:0.5.66 |
| audit-service | ghcr.io/cnoe-io/caipe-audit-service:0.5.66 |
| agentgateway | ghcr.io/agentgateway/agentgateway:v1.1.0 |
| agentgateway-config-bridge | ghcr.io/cnoe-io/agentgateway-config-bridge:0.5.66 |
| keycloak | quay.io/keycloak/keycloak:26.3 |
| openfga | openfga/openfga:latest (unpinned) |
| openfga-authz-bridge | built locally: ai-platform-engineering-openfga-authz-bridge |
| langfuse-web / worker | langfuse/langfuse:3, langfuse/langfuse-worker:3 |
| milvus-standalone | milvusdb/milvus:v2.5.14 |
| caipe-mongodb | mongo:7.0 |
| cloudflared | cloudflare/cloudflared:latest (unpinned) |
| github-mcp-server | ghcr.io/github/github-mcp-server:latest (defined in compose, not running: `ENABLE_GITHUB=false`) |

Unpinned: `openfga/openfga:latest`, `cloudflared:latest`, `github-mcp-server:latest`. Pin digests before the event.

## Host

- 15 GiB RAM total, about 6.4 GiB in use by the CAIPE stack, about 9 GiB available (Phase 1 adds a kind cluster)
- Docker, kind and kubectl installed; `gh` and `make` are not installed

## Ports

caipe-ui 3000, langfuse-web 3100, dynamic-agents 8100, rag-server 9446, agentgateway 4000, keycloak 7080 (localhost only), openfga 18080 (localhost only)

## Models

LLM provider is `openai` (`LLM_PROVIDER` in the install's `.env`). Model names for providers A and B in the swap are still open (spec section 10).

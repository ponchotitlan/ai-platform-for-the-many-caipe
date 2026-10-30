# AGENTS.md

Guidance for coding agents (VS Code, GitHub Copilot, Cursor, Codex, Gemini CLI, Claude Code and others) working in this repository.

## What this repository is

**Incident Copilot** is a demo built on [CAIPE](https://caipe.io/) (Community AI Platform Engineering). A customer ticket in Jira is investigated by a team of AI agents, and a person approves every change. Start with the [README](README.md), then the [setup and running guide](docs/README.md).

There is no application code to build here besides a tiny fictional app (LedgerLite). Most of the project is **configuration written as readable files**: agent definitions, prompts, a skill, knowledge-base documents, Kubernetes manifests and shell scripts.

## Where things live

| Path | What it holds |
| --- | --- |
| `config/seed/*.yaml` | Reference copies of the agents and tool servers. **Not loaded by CAIPE**: a person creates each one by hand in the CAIPE UI. The prompts live here. |
| `config/policy.yaml` | A readable map of who can reach what and where each rule is enforced. CAIPE does not read it. |
| `skills/jira-board/SKILL.md` | The shared skill used by two agents. |
| `kb/` | 20 synthetic knowledge documents (`RB-*` runbooks, `PM-*` past incidents, `PD-*` product docs). |
| `incident-copilot-demo/` | LedgerLite: services, Kubernetes manifests (`app/k8s/`), compose files for the tool servers, helper scripts. |
| `docs/` | The setup and running guide, with room for screenshots. |
| `observability/` | The observability stack and its own guide. |

## Dev environment tips

- **Shell scripts** (`incident-copilot-demo/scripts/*.sh`) use `bash` with `set -euo pipefail`. Keep that, and check syntax with `bash -n <script>`.
- **LedgerLite services** are plain Python 3.12 using only the standard library, in `incident-copilot-demo/app/services/`. Do not add dependencies without a reason.
- **YAML** (seeds, policy, manifests): validate after editing, for example:
  ```bash
  python3 -c "import yaml,sys; [yaml.safe_load(open(f)) for f in sys.argv[1:]]; print('ok')" config/seed/*.yaml config/policy.yaml
  ```
- **Tools you will meet**: Docker, `kind`, `kubectl`, `bash`. The CAIPE install itself lives outside this repository.

### Quick run examples

From the repository root, with the cluster and CAIPE already running:

```bash
incident-copilot-demo/scripts/reset-fault.sh   # plant the bad rollout (checkout-api v1.4.0)
incident-copilot-demo/scripts/traffic.sh       # generate requests so the cluster shows symptoms
incident-copilot-demo/scripts/fix-fault.sh     # roll checkout-api back to v1.3.2
incident-copilot-demo/scripts/mcp-up.sh        # read-only Kubernetes tool server
incident-copilot-demo/scripts/mcp-ops-up.sh    # write-enabled server (Deployment update only)
```

## Documentation and tool references

- CAIPE: <https://caipe.io/> and <https://github.com/caipe-io/ai-platform-engineering>
- Kubernetes MCP server (upstream, used as is): <https://github.com/containers/kubernetes-mcp-server>
- Model Context Protocol: <https://modelcontextprotocol.io/>
- Jira Cloud REST API: <https://developer.atlassian.com/cloud/jira/platform/rest/v3/>
- MCP servers this project uses: `k8s-readonly`, `k8s-ops` (Kubernetes) and `jira`. Their registration values are in `config/seed/mcp_servers.seed.yaml`.
- No Cisco DevNet sandbox is needed: the cluster is a local `kind` cluster and the tickets are in a Jira Cloud project.

## Testing instructions

There is no automated test suite yet. Check changes like this:

- **Seeds and policy**: validate the YAML (above), and make sure every tool named in an agent's `allowed_tools` exists on the server named next to it.
- **Cluster identities**: after changing RBAC, prove it with `kubectl auth can-i` (the commands are in the [setup guide](docs/README.md), section 3.2). The write account must be able to patch Deployments in `ledgerlite` and nothing else.
- **Agent behavior**: prompts are tested by hand in the CAIPE UI, one fresh chat per question, and by reading the tool calls, not only the answer. Keep the question list you test with in the pull request.
- **Knowledge documents**: each `##` section keeps its italic ID line (`*RB-02 · title · updated date*`), and `PD-*` documents contain no internal service names.

## PR instructions

- **Security**: do not commit real credentials, tokens or personal data. Keep secrets in the CAIPE install's environment, never in this repository. Customers in demo tickets are fictional and use reserved example domains.
- **Never read, print or copy secrets** (environment files, kubeconfigs, password files) into logs, chat or commits.
- **Record decisions**: any fake, deviation, workaround or trade-off is written down in the pull request description, with the reason.
- **Say what you verified**: state what you ran and what you only read. Do not claim an agent behavior works until it has run in the UI.
- Follow the [contributing guide](CONTRIBUTING.md).

## Contribution conventions

- **Seeds are the source of truth for prompts.** When you change an agent's prompt, change it in `config/seed/` and say that the running agent must be updated by hand in the UI.
- **Prompts are not security.** A rule that matters (who can write, which tickets are visible) must be enforced by CAIPE permissions, tool lists, approvals or cluster RBAC, and the prompt only reinforces it. When something is only a convention, say so.
- **Least privilege by name.** Give each agent only the tools it needs, listed one by one. Writes always go behind an approval.
- **Verify against what runs, not what you read.** The running CAIPE images are `0.5.66`, while a CAIPE source checkout may be a newer version with features the images do not have. Check the running container before relying on a behavior.
- **Ask before** starting third-party containers, changing identity or access settings, or writing to the shared Jira project.
- **Backward compatibility**: do not change existing behavior unless clearly improving or fixing a bug, and document changes in the pull request.

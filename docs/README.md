# 🛠️ Setup and walkthrough

How to build the demo on top of a running CAIPE, piece by piece, and what it looks like when it works.
Then a step-by-step tour of what each person does with it.

**On this page**
1. [What you need first](#1--what-you-need-first)
2. [Build order](#2--build-order)
3. [Setup, component by component](#3--setup-component-by-component)
4. [The walkthrough: who does what, in order](#4--the-walkthrough-who-does-what-in-order)

---

## 🗺️ Find your way around

The following are the files and folders from this repository that we will work with:

| 📁 Folder | What is inside |
| --- | --- |
| [`config/seed/`](../config/seed/) | The agents and tool servers, written out as readable YAML (reference copies, created by hand in the UI). |
| [`skills/`](../skills/) | The shared `jira-board` skill. |
| [`kb/`](../kb/) | The 20 knowledge documents: runbooks, past incidents, product docs. |
| [`incident-copilot-demo/`](../incident-copilot-demo/) | LedgerLite: the app, its Kubernetes manifests, and the helper scripts. |
| [`docs/`](./) | The full spec, every decision and trade-off, and the step-by-step guides. |

---

## 1. 🧰 What you need first

This guide starts **after** CAIPE is already running, signed in as an admin. It also assumes:

| ✔ | Already in place | Where it comes from |
| --- | --- | --- |
| ☐ | A running CAIPE with its chat UI, sign-in, teams and knowledge-base (RAG) service | your CAIPE install |
| ☐ | An OpenAI model available to CAIPE (`GPT-4o`, optionally `GPT-4o mini`) | your CAIPE model list |
| ☐ | A local Kubernetes cluster running **LedgerLite** with its fault planted | [`incident-copilot-demo/scripts/`](../incident-copilot-demo/scripts/) (`up.sh`, `reset-fault.sh`, `traffic.sh`) |
| ☐ | A Jira Cloud project (`AIPLATFORM`) and API credentials in the CAIPE install's environment | your Atlassian account |
| ☐ | The Jira MCP server container that ships with CAIPE, running | the install's `jira` profile |

> 🧪 **Reference seeds, not auto-loaded.** Everything in [`config/seed/`](../config/seed/) is a readable copy of what you type into the UI.
> You create each piece by hand, so you can show it on stage. Prompts live in the seed files: copy them from there.

---

## 2. 🧭 Build order

Some pieces need others to exist first. Follow this order.

```mermaid
flowchart TD
    A["1️⃣ Models<br/>GPT-4o"] --> D
    B["2️⃣ Tool servers<br/>👀 k8s read-only · ✍️ k8s update · 🎫 Jira"] --> D
    C["3️⃣ Knowledge bases<br/>🔴 runbooks · 🟠 incidents · 🟢 product docs"] --> D
    S["4️⃣ Shared skill<br/>🧩 jira-board"] --> D
    D["5️⃣ Agents<br/>📚 Knowledge · ☸️ Cluster · 🎧 Support · 🧭 Incident Copilot"] --> E
    E["6️⃣ People and teams<br/>🎧 support · 🧑‍🔧 oncall · 🔎 owner"] --> F
    F["7️⃣ Access grants<br/>who sees which agent and knowledge base"] --> G
    G["8️⃣ Demo tickets in Jira<br/>🏷️ demo-ledgerlite"]
```

Inside step 5, create the agents in this order: **Knowledge Agent → Cluster Agent → Support Agent → Incident Copilot**.
The Incident Copilot lists the first two as sub-agents, so they must exist when you get to it.

---

## 3. 🧱 Setup, component by component

Menu names can differ a little between CAIPE versions. Field values below are exactly what the seeds contain.

### 3.1 🤖 Models

| | |
| --- | --- |
| **Seed** | the `models:` list in your CAIPE install's own `config/app-config.yaml` (it lives in the CAIPE install, not in this repo) |
| **Where** | Admin → LLM Models (or the app config the UI seeds from) |
| **Values** | `GPT-4o (OpenAI)` → model id `gpt-4o`, provider `openai`. Optionally `GPT-4o Mini (OpenAI)` → `gpt-4o-mini` for the model-swap beat |

✅ **Check:** both models appear in the model picker when you create an agent.

![CAIPE LLM](images/01-caipe-llm.png)

---

### 3.2 🔧 Tool servers (MCP)

Create three servers under **Agents → MCP Servers → Add MCP Server** (choose the manual option). Seed: [`config/seed/mcp_servers.seed.yaml`](../config/seed/mcp_servers.seed.yaml).

| Name | ID | URL | Transport | What it is |
| --- | --- | --- | --- | --- |
| `Kubernetes (read-only)` | `k8s-readonly` | `http://k8s-readonly-mcp:8000/mcp` | HTTP | Upstream Kubernetes MCP server, read-only, with a read-only cluster account |
| `Kubernetes (Deployment update)` | `k8s-ops` | `http://k8s-ops-mcp:8000/mcp` | HTTP | Same upstream server with writes enabled and a separate account that may only `get`, `list`, `patch`, `update` Deployments in `ledgerlite` |
| `Jira` | `jira` | `http://mcp-jira:8000/mcp` | HTTP | CAIPE's bundled Jira server. Credentials come from the install's environment, so **leave the credential sources empty** |

**Start the two cluster servers first** (from the repo root):

```bash
incident-copilot-demo/scripts/mcp-up.sh        # 👀 read-only server and its read-only account
incident-copilot-demo/scripts/mcp-ops-up.sh    # ✍️ write-enabled server and its Deployment-only account
```

**Prove the write account is narrow** before you register `k8s-ops`:

```bash
KC=incident-copilot-demo/.kube/agent-ops.kubeconfig
kubectl --kubeconfig $KC auth can-i patch  deployments -n ledgerlite   # yes
kubectl --kubeconfig $KC auth can-i delete deployments -n ledgerlite   # no
kubectl --kubeconfig $KC auth can-i get    secrets     -n ledgerlite   # no
kubectl --kubeconfig $KC auth can-i patch  deployments -n kube-system  # no
```

✅ **Check:** probe each server in the UI.
- `k8s-readonly` lists read tools only (`pods_list_in_namespace`, `pods_get`, `pods_log`, `events_list`, `resources_list`, `resources_get`, and a few more).
- `k8s-ops` lists `resources_create_or_update` **and** delete, exec and run tools. That is expected: Kubernetes refuses the extra ones for this account, and each agent's tool list only allows one.
- `jira` lists about 62 tools. Agents will each be allowed only a handful.

![CAIPE MCP](images/02-caipe-mcp.png)

![CAIPE Probe](images/03-caipe-mcp-probe.png)

---

### 3.3 📚 Knowledge bases

Twenty synthetic markdown documents in [`kb/`](../kb/). **One upload per folder**, so each folder becomes its own datasource and can have its own owners.

| Folder | Documents | Datasource name | Who may see it |
| --- | --- | --- | --- |
| [`kb/runbooks`](../kb/runbooks/) | RB-01 to RB-08 | `ledgerlite-runbooks` | oncall, owner |
| [`kb/incidents`](../kb/incidents/) | PM-01 to PM-06 | `ledgerlite-incidents` | oncall, owner |
| [`kb/product_docs`](../kb/product_docs/) | PD-01 to PD-06 | `ledgerlite-product-docs` | support, oncall, owner |

Steps (Knowledge Bases page): add a source from local files, select all files of one folder, set a description, **chunk size 800, overlap 100**, upload, wait for ingestion, repeat for the other two.

✅ **Check:** the three datasources show 8, 6 and 6 documents.

![CAIPE Knowledge Base](images/04-caipe-knowledge-base.png)

---

### 3.4 🧩 The shared skill

A skill is a markdown instruction document that agents load. **It teaches a procedure; it grants no tools.**

| | |
| --- | --- |
| **Source** | [`skills/jira-board/SKILL.md`](../skills/jira-board/SKILL.md) |
| **Where** | Skills → Create skill |
| **Name** | `jira-board` |
| **Content** | Paste the file. Description is the `description:` line of its header, the rest is the body |

✅ **Check:** the card has Edit and Delete enabled, and *Open Files* lists `SKILL.md`.

![CAIPE Skills](images/05-caipe-skills.png)

![CAIPE Edit Skill](images/06-caipe-skill-edit.png)

---

### 3.5 🤖 The four agents

**Agents → Create Agent.** For each agent: name, description, model `GPT-4o (OpenAI)`, the **system prompt copied from its seed**, then tools and visibility as below.

#### 📚 Knowledge Agent
Seed: [`config/seed/agents.knowledge.seed.yaml`](../config/seed/agents.knowledge.seed.yaml)

| Setting | Value |
| --- | --- |
| Tools | `knowledge-base`: `search`, `fetch_document` |
| Approval | none |
| Sub-agents / skills | none |
| Visibility | Team: `oncall`, `owner` |

#### ☸️ Cluster Agent
Seed: [`config/seed/agents.cluster.seed.yaml`](../config/seed/agents.cluster.seed.yaml)

| Setting | Value |
| --- | --- |
| Tools | `k8s-readonly`: the six read tools · `k8s-ops`: **`resources_create_or_update` only** |
| Approval | **required** on `k8s-ops` → `resources_create_or_update` (approve, edit, reject) |
| Sub-agents / skills | none |
| Visibility | Team: `oncall`, `owner` |

#### 🎧 Support Agent
Seed: [`config/seed/agents.support.seed.yaml`](../config/seed/agents.support.seed.yaml)

| Setting | Value |
| --- | --- |
| Tools | `knowledge-base`: `search`, `fetch_document` · `jira`: `get_issue`, `search` |
| Approval | none (it has no write tool) |
| Skills | `jira-board` |
| Visibility | Team: `support`, `owner` |

#### 🧭 Incident Copilot
Seed: [`config/seed/agents.seed.yaml`](../config/seed/agents.seed.yaml)

| Setting | Value |
| --- | --- |
| Tools | `jira`: `get_issue`, `search`, `add_comment`, `get_transitions`, `transition_issue`. **No cluster or knowledge tools of its own** |
| Approval | **required** on `jira` → `transition_issue` (approve, edit, reject). `add_comment` runs without approval |
| Skills | `jira-board` |
| Sub-agents | **Cluster Agent** (`cluster-agent`) and **Knowledge Agent** (`knowledge-agent`), with the descriptions from the seed |
| Visibility | Team: `oncall`, `owner` |

✅ **Check:** the agent list shows four agents. Open the Incident Copilot: its tool list has only Jira tools, and its sub-agents are the Cluster Agent and the Knowledge Agent.

![CAIPE Agents](images/07-caipe-agents.png)

![CAIPE MCP Tools](images/10-caipe-mcp-tools.png)

![CAIPE Subagents](images/08-caipe-agent-subagents.png)

![CAIPE Human Approval](images/09-caipe-human-approval.png)

---

### 3.6 👥 People and teams

**Three users**, created in the identity provider (Keycloak) of your CAIPE, each signing in to the UI **once** so they show up in the team search:

| Persona | User | Team |
| --- | --- | --- |
| 🎧 Support | `joao.silva` | `support` |
| 🧑‍🔧 On-call | `beatriz.santos` | `oncall` |
| 🔎 Owner | `miguel.ferreira` | `owner` |

Then **Admin → Teams → Create Team** for `support`, `oncall` and `owner`, and add each user to their team.

![CAIPE Teams](images/11-caipe-teams.png)

---

### 3.7 🔐 Access grants

Open each team's details and set what it can reach. This is what makes the same question behave differently per person.

| Team | Agents | Knowledge bases |
| --- | --- | --- |
| `support` | Support Agent | `ledgerlite-product-docs` |
| `oncall` | Incident Copilot, Cluster Agent, Knowledge Agent | all three |
| `owner` | all four | all three |

If an agent or tool server is not offered for a team, check the agent's visibility and the team's tool-server grants (the `knowledge-base`, `jira`, `k8s-readonly` and `k8s-ops` servers).

✅ **Check:** log in as `joao.silva` in a private window. The agent picker lists **only the Support Agent**.

---

### 3.8 🎫 Demo tickets in Jira

Create a ticket in project `AIPLATFORM`, type **Task**, status **To Do**, with the label **`demo-ledgerlite`**. Write them the way a customer would: no internal service names, and fictional customers on a reserved domain such as `example.com`.

```text
Summary:     Customer cannot pay invoice - checkout keeps failing
Description: Customer: Indira Leão (indira@example.com)
             Reporter: customer on the LedgerLite web app (invoice INV-1007).
             What happened: pressing "Pay" spins and then shows "Something went wrong". Started around 16:00, still failing.
             Impact: the customer cannot pay; other customers report the same.
             Already tried: reloading, another browser.
```

The first line, `Customer: <name> (<email>)`, is what the Support Agent reads.

Also create **one ticket without the label**, to prove the agents leave it alone.

**Make the outage visible:** run `incident-copilot-demo/scripts/reset-fault.sh`, then `incident-copilot-demo/scripts/traffic.sh`.

![JIRA board](images/12-jira-board.png)

---

## 4. 🎭 The walkthrough: who does what, in order

The demo, told as a story: a customer cannot pay, support answers safely, the on-call engineer diagnoses and a person approves every change, and the owner sees the whole picture.

👉 **[Read the walkthrough story](walkthrough/README.md)**

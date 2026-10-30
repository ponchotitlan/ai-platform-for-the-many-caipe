<div align="center">

# 🧠🧩⚙️ AI Platforming For The Many

**A hands-on demo of [CAIPE](https://github.com/caipe-io/ai-platform-engineering) (Community AI Platform Engineering)**
for the talk *Democratising AI Platform Engineering with Open Source: Own It, Run It, Trust It*

</div>

<div align="center">

<p>
  <img src="https://img.shields.io/badge/CAIPE-0.5.66-6F42C1?style=flat&labelColor=555555&logoColor=white" alt="CAIPE 0.5.66"/>
  <img src="https://img.shields.io/badge/MCP-tool%20servers-1F1F1F?style=flat&logo=modelcontextprotocol&labelColor=555555&logoColor=white" alt="MCP tool servers"/>
  <img src="https://img.shields.io/badge/AgentGateway-v1.1.0-E5532D?style=flat&labelColor=555555&logoColor=white" alt="AgentGateway v1.1.0"/>
  <img src="https://img.shields.io/badge/Keycloak-26.3-4D4D4D?style=flat&logo=keycloak&labelColor=555555&logoColor=white" alt="Keycloak 26.3"/>
  <img src="https://img.shields.io/badge/OpenFGA-latest-1F6FEB?style=flat&labelColor=555555&logoColor=white" alt="OpenFGA latest"/>
  <img src="https://img.shields.io/badge/OpenAI-GPT--4o-412991?style=flat&logo=openai&labelColor=555555&logoColor=white" alt="OpenAI GPT-4o"/>
  <img src="https://img.shields.io/badge/OpenAI-GPT--4o%20mini-412991?style=flat&logo=openai&labelColor=555555&logoColor=white" alt="OpenAI GPT-4o mini"/><br/>
  <img src="https://img.shields.io/badge/Milvus-v2.5.14-00A1EA?style=flat&logo=milvus&labelColor=555555&logoColor=white" alt="Milvus v2.5.14"/>
  <img src="https://img.shields.io/badge/MongoDB-7.0-47A248?style=flat&logo=mongodb&labelColor=555555&logoColor=white" alt="MongoDB 7.0"/>
  <img src="https://img.shields.io/badge/Redis-7-DC382D?style=flat&logo=redis&labelColor=555555&logoColor=white" alt="Redis 7"/>
  <img src="https://img.shields.io/badge/PostgreSQL-16-4169E1?style=flat&logo=postgresql&labelColor=555555&logoColor=white" alt="PostgreSQL 16"/><br/>
  <img src="https://img.shields.io/badge/Docker-29.9.2-2496ED?style=flat&logo=docker&labelColor=555555&logoColor=white" alt="Docker 29.9.2"/>
  <img src="https://img.shields.io/badge/kind-v0.33.0-326CE5?style=flat&logo=kubernetes&labelColor=555555&logoColor=white" alt="kind v0.33.0"/>
  <img src="https://img.shields.io/badge/Kubernetes-v1.37-326CE5?style=flat&logo=kubernetes&labelColor=555555&logoColor=white" alt="Kubernetes v1.37"/>
  <img src="https://img.shields.io/badge/kubectl-v1.37.1-326CE5?style=flat&logo=kubernetes&labelColor=555555&logoColor=white" alt="kubectl v1.37.1"/>
  <img src="https://img.shields.io/badge/Kubernetes%20MCP%20server-v0.0.67-326CE5?style=flat&logo=kubernetes&labelColor=555555&logoColor=white" alt="Kubernetes MCP server v0.0.67"/>
  <img src="https://img.shields.io/badge/Jira%20MCP%20server-0.5.66-0052CC?style=flat&logo=jira&labelColor=555555&logoColor=white" alt="Jira MCP server 0.5.66"/>
  <img src="https://img.shields.io/badge/Jira-Cloud-0052CC?style=flat&logo=jira&labelColor=555555&logoColor=white" alt="Jira Cloud"/><br/>
  <img src="https://img.shields.io/badge/Python-3.13%20agents-3776AB?style=flat&logo=python&labelColor=555555&logoColor=white" alt="Python 3.13 agents"/>
  <img src="https://img.shields.io/badge/Python-3.12%20LedgerLite-3776AB?style=flat&logo=python&labelColor=555555&logoColor=white" alt="Python 3.12 LedgerLite"/>
  <img src="https://img.shields.io/badge/Node.js-24%20UI-5FA04E?style=flat&logo=nodedotjs&labelColor=555555&logoColor=white" alt="Node.js 24 UI"/>
</p>

</div>

---

## 🧠 What is CAIPE?

**CAIPE** (pronounced like *cape* 🦸) is an open-source AI platform for building, deploying, governing and operating AI agents and agentic workflows for platform engineering and beyond. You create **agents** (an LLM plus instructions plus a set of tools), give them **knowledge** and **permissions**, and let people talk to them in a chat UI.

Think of it as the **workshop**, not the product: you bring the problem, the documents and the rules, and CAIPE gives you the parts to assemble a team of agents.

### ⚡ Capabilities in a nutshell

```mermaid
mindmap
  root((🧠 CAIPE))
    🤖 Agents
      Created from the web UI
      Any supported LLM
      Sub-agents that delegate
    🔧 Tools through MCP
      Kubernetes, Jira, GitHub and more
      One server per system
      Each agent gets only the tools you list
    📚 Knowledge
      Upload or connect documents
      Cited answers
      One datasource per owner
    🧩 Skills
      Reusable instructions
      Shared between agents
      Teach a procedure, grant no tools
    🔐 People and permissions
      Single sign-on
      Teams
      Who can use which agent or knowledge base
    🙋 Human in the loop
      Approval before a risky tool call
      Approve, edit or reject
```

| | Capability | What it means for you |
| --- | --- | --- |
| 🤖 | **Dynamic agents** | Create and change agents in the UI. An agent is data, not code. |
| 🔧 | **MCP tools** | Plug in systems through the Model Context Protocol, and pick tool by tool what each agent may call. |
| 📚 | **Knowledge bases (RAG)** | Documents are split, indexed and searched. Answers can cite the document they came from. |
| 🧩 | **Skills** | Write a procedure once in a markdown file and give it to several agents. |
| 👥 | **Teams and access** | Users sign in once. Teams decide which agents and knowledge bases they can reach. |
| ✋ | **Approvals** | Mark a tool as "ask first". The run pauses on a card until a person decides. |
| 🔀 | **Sub-agents** | An agent can hand part of a job to a specialist and use what comes back. |

---

## 🎬 This demo: the story

**LedgerLite** is a small, **fictional** invoicing and card-payments product running on a Kubernetes cluster. A release went out twenty-five minutes ago. Since then, paying an invoice spins and fails.

```mermaid
flowchart LR
    A["😟 Customer<br/>can't pay"] --> B["🎫 Jira ticket"]
    B --> C["🤖 AI agents<br/>investigate"]
    C --> D["📝 Diagnosis<br/>on the ticket"]
    D --> E{"🙋 Human<br/>approves?"}
    E -- "✅ yes" --> F["🚀 Ticket moves on"]
    E -- "❌ no" --> G["🛑 Nothing changes"]
```

This is the workflow:

```mermaid
sequenceDiagram
    autonumber
    participant C as 😟 Indira (customer)
    participant J as 🎫 Jira
    participant S as 🎧 João (support)
    participant O as 🧑‍🔧 Beatriz (on-call)
    participant P as 🤖 Incident Copilot
    participant K as ☸️ Cluster Agent
    participant L as 📚 Knowledge Agent

    C->>J: Reports "I can't pay my invoice"
    S->>J: Asks the Support Agent for the open tickets
    Note over S,J: 🎧 The Support Agent reads the ticket<br/>and drafts a friendly, safe reply
    O->>P: "Work on this ticket"
    P->>K: Investigate the cluster (read-only)
    K-->>P: Checkout restarts, failing probes, a timeout changed 5000 to 500
    P->>L: What do our runbooks and past incidents say?
    L-->>P: Cited answer, and a warning that two documents disagree
    P->>J: Adds the diagnosis as a comment
    P->>O: Asks to move the ticket to In Progress
    O-->>P: ✅ Approve
    P->>J: Ticket moves to In Progress
    O->>K: In the Cluster Agent chat: "Roll back the deploy"
    K->>O: Shows the exact change and waits
    O-->>K: ❌ Reject (nothing changes)
```

### 🪤 What is planted for you to find

| 🎯 The trap | What it tests |
| --- | --- |
| **A bad rollout.** `checkout-api` v1.4.0 changed a timeout from 5000 ms to 500 ms. The mock payment gateway answers in 2 to 5 seconds, so most payments fail. | Can the agents find the *real* cause? |
| **Two red herrings.** The runbooks about *database connections* and *payment provider outages* look relevant, but the checks come back normal. | Do the agents stay calm and rule things out? |
| **Contradicting documents.** An old runbook says "restart the pod first". A newer postmortem says restarting made it worse. | Does the agent show both and say which it prefers? |
| **A shared Jira project.** Other people's tickets live next to the demo ones. | Do the agents stay in their lane? |

---

## 🎭 The actors

Everyone in this story is made up. Customers use reserved example domains.

### 👥 The humans

| | Who | Role | Can do |
| --- | --- | --- | --- |
| 😟 | **Indira** | Customer | Reports the problem. In the demo, a person creates her ticket by hand; a small mock web app comes later. |
| 🎧 | **João** | **Support** | Reads tickets, drafts customer replies from product documents. Never sees cluster data or internal runbooks. |
| 🧑‍🔧 | **Beatriz** | **On-call engineer** | Has the Incident Copilot investigate tickets, approves status changes, and can troubleshoot the cluster directly. |
| 🔎 | **Miguel** | **Owner** | Sees everything, reviews what the agents did. |

### 🤖 The agents

| | Agent | Job | Its tools | Its one write |
| --- | --- | --- | --- | --- |
| 🧭 | **Incident Copilot** | Resolves a ticket end to end | Jira (read, comment, move) + two sub-agents | Moves a ticket from *To Do* to *In Progress*, **after approval** |
| ☸️ | **Cluster Agent** | Investigates the cluster, and is the on-call's chat for troubleshooting | Read-only Kubernetes tools + one write | Updates **one Deployment**, **after approval** |
| 📚 | **Knowledge Agent** | Answers from the runbooks, past incidents and product docs, with citations | Search and read documents | None |
| 🎧 | **Support Agent** | Turns a ticket into a friendly, customer-safe reply | Jira (read only) + product docs | **None** |

---

## 🧱 The components

```mermaid
flowchart TB
    subgraph PEOPLE["👥 People"]
        direction LR
        U1["🎧 Support"]
        U2["🧑‍🔧 On-call"]
        U3["🔎 Owner"]
    end

    subgraph CAIPE["🧠 CAIPE"]
        direction TB
        UI["💬 Chat UI<br/>sign-in, teams, approvals"]
        subgraph AGENTS["🤖 Agents"]
            direction LR
            IC["🧭 Incident Copilot"]
            CA["☸️ Cluster Agent"]
            KA["📚 Knowledge Agent"]
            SA["🎧 Support Agent"]
        end
        SK["🧩 Shared skill<br/>jira-board"]
        RAG["🗄️ Knowledge bases<br/>🔴 runbooks · 🟠 past incidents · 🟢 product docs"]
    end

    subgraph TOOLS["🔧 Tool servers (MCP)"]
        direction LR
        T1["🎫 Jira"]
        T2["👀 Kubernetes<br/>read-only"]
        T3["✍️ Kubernetes<br/>one Deployment update"]
    end

    subgraph WORLD["🌍 The outside world"]
        direction LR
        JIRA[("🎫 Jira Cloud<br/>board AIPLATFORM")]
        APP[("☸️ Kubernetes cluster<br/>🧾 LedgerLite app")]
    end

    PEOPLE --> UI --> AGENTS
    SK -.-> IC
    SK -.-> SA
    IC --> CA
    IC --> KA
    KA --> RAG
    SA --> RAG
    IC --> T1
    SA --> T1
    CA --> T2
    CA --> T3
    T1 --> JIRA
    T2 --> APP
    T3 --> APP
```

| | Component | What it is |
| --- | --- | --- |
| 🧾 | **LedgerLite** | A tiny made-up app of four services (`web-frontend`, `checkout-api`, `payments-gateway`, `postgres`) on a local Kubernetes cluster, with one deliberate fault. |
| 📚 | **Knowledge bases** | 20 short markdown documents written for LedgerLite: 🔴 8 runbooks, 🟠 6 past incidents, 🟢 6 product docs. Each is its own datasource, so each can have its own owners. |
| 🎫 | **Jira board** | Project `AIPLATFORM`. Demo tickets carry the label `demo-ledgerlite` and move through *To Do → In Progress → Done*. |
| 🧩 | **Shared skill** | `jira-board` tells two different agents how to read the board safely. One skill, two agents, two sets of permissions. |
| 👀 | **Read-only Kubernetes tools** | The upstream Kubernetes MCP server in read-only mode, with a cluster account that can only look. |
| ✍️ | **Deployment-update tool** | A second instance of the same upstream server, with a separate cluster account that may update Deployments in one namespace and nothing else. |
| 👥 | **Teams** | `support`, `oncall`, `owner`. Teams decide who can use which agent and knowledge base. |

---

## 🔗 How the pieces relate

### 🔀 Who calls whom

```mermaid
flowchart LR
    IC["🧭 Incident Copilot<br/>reads and writes the ticket"]
    CA["☸️ Cluster Agent<br/>cluster evidence"]
    KA["📚 Knowledge Agent<br/>cited documents"]
    SA["🎧 Support Agent<br/>customer reply"]

    IC -- "asks: what is wrong?" --> CA
    IC -- "asks: what do our docs say?" --> KA
    SA -. "searches product docs" .-> KA
    CA -- "🙋 asks first" --> W1[("✍️ Update one Deployment")]
    IC -- "🙋 asks first" --> W2[("🎫 Move the ticket")]
```

The Incident Copilot has **no cluster tools of its own**. It can only ask the Cluster Agent, and it is told never to ask it to change anything. Changes happen in the Cluster Agent's own chat, with a person watching.

### 🔐 Who can reach what

| | 🎧 Support | 🧑‍🔧 On-call | 🔎 Owner |
| --- | :---: | :---: | :---: |
| 🎧 Support Agent | ✅ | ❌ | ✅ |
| 🧭 Incident Copilot | ❌ | ✅ | ✅ |
| ☸️ Cluster Agent | ❌ | ✅ | ✅ |
| 📚 Knowledge Agent | ❌ | ✅ | ✅ |
| 🟢 Product docs | ✅ | ✅ | ✅ |
| 🔴 Runbooks · 🟠 Past incidents | ❌ | ✅ | ✅ |

> The same question asked by two people gets different sources, different tools and a different answer, because the platform, not the prompt, decides what each person can reach.

### 🎫 The life of a ticket

```mermaid
stateDiagram-v2
    direction LR
    state "📝 To Do" as todo
    state "🔧 In Progress" as wip
    state "🏁 Done" as done

    [*] --> todo: 😟 customer reports
    todo --> wip: 🤖 Copilot diagnoses, 🙋 a person approves
    wip --> done: 🧑 a person closes it
```

The agents never close tickets. *Done* belongs to humans.

---

## 🛡️ Why you can trust it

| 🧱 Guardrail | How it works |
| --- | --- |
| ✋ **Approval before every change** | The two writes (move a ticket, update a Deployment) pause on an approval card that shows the exact call. Approve, edit or reject. |
| 🎯 **Few tools, by name** | Jira offers about 62 tools. The Copilot may use five, and the Support Agent two. |
| 👀 **Reads and writes use different identities** | The cluster account that reads cannot write, and the one that writes can only touch Deployments in one namespace. |
| 👥 **Access is a team setting** | Support cannot reach the runbooks or the cluster agents, whatever the prompt says. |
| 🧩 **Tickets are data, not orders** | If a ticket says "ignore your rules", the agents are told to ignore *that* and say so. |
| 🔍 **Honest about limits** | The agents are told to say what they could not check, and the knowledge agent flags when two documents disagree. |

---

## 📚 Guides and links

| | Guide | What you get |
| --- | --- | --- |
| 🛠️ | [**Setup and running guide**](docs/README.md) | How to set up each component on a running CAIPE, what the finished UI looks like, and a step-by-step walkthrough of each persona, with room for your screenshots. |
| 🔭 | [**Observability guide**](observability/README.md) | Where CAIPE's telemetry comes from, and how it is collected and shown in Splunk. |
| 🌐 | [**CAIPE website**](https://caipe.io/) | The CAIPE project itself: documentation, community and getting started. |

---

<div align="center"><br />
    Made with ☕️ by Poncho Sandoval - <code>Developer Advocate 🥑 @ DevNet - Cisco Systems 🇵🇹</code><br /><br />
    <a href="mailto:alfsando@cisco.com?subject=Question%20about%20CAIPE&body=Hello,%0A%0AI%20have%20a%20question%20regarding%20your%20project.%0A%0AThanks!">
        <img src="https://img.shields.io/badge/Contact%20me!-blue?style=flat&logo=gmail&labelColor=555555&logoColor=white" alt="Contact Me via Email!"/>
    </a>
    <a href="https://github.com/ponchotitlan/ai-platform-for-the-many-caipe/blob/main/CONTRIBUTING.md">
      <img src="https://img.shields.io/badge/Open%20Issue-2088FF?style=flat&logo=github&labelColor=555555&logoColor=white" alt="Open an Issue"/>
    </a>
    <a href="https://github.com/ponchotitlan/ai-platform-for-the-many-caipe/fork">
      <img src="https://img.shields.io/badge/Fork%20Repository-000000?style=flat&logo=github&labelColor=555555&logoColor=white" alt="Fork Repository"/>
    </a>
</div>

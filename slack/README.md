# 💬 CAIPE in Slack: talk to your agents from a channel

*The agents do not change. The front door does: the same Support, the same teams and the same approvals, reached from a Slack channel instead of the web UI.*

CAIPE ships a Slack bot. This guide wires it to the **Support** demo, so an on-call engineer can ask about a ticket from `#caipe` and get the answer in a thread. It also records every trap hit while doing it on a docker compose install, with the fix for each.

**On this page**
1. [The idea in one page](#1--the-idea-in-one-page)
2. [What you need first](#2--what-you-need-first)
3. [Setup, step by step](#3--setup-step-by-step)
4. [Run it and check it](#4--run-it-and-check-it)

---

## 1. 🧭 The idea in one page

```mermaid
flowchart LR
    U["🧑‍🔧 Support User<br/>in #caipe"] --> S["💬 Slack"]
    S -- "Socket Mode<br/>(the bot dials out)" --> B["🤖 slack-bot<br/>container"]
    B -- "http://caipe-ui:3000" --> UI["💬 CAIPE UI / BFF<br/>access checks"]
    UI --> DA["🧭 dynamic-agents<br/>Support"]
    DA -- "via AgentGateway" --> T["🔧 Tool servers (MCP)<br/>Jira · Kubernetes · Knowledge base"]
    B -. "who is this Slack user?" .-> KC["🔐 Keycloak"]
```

| | Piece | What it does |
| --- | --- | --- |
| 🤖 | **`slack-bot`** | A Slack app running as one more container. In **Socket Mode** it opens an outbound connection to Slack, so you need **no public URL** for it. Your Cloudflare tunnel is untouched. |
| 🗺️ | **Channel route** | Each Slack channel is mapped to one agent and one team. A mention in `#caipe` goes to the Support. |
| 🧑 | **Identity** | The bot finds the Keycloak user behind the Slack user and calls CAIPE **as that person** (on-behalf-of). Teams, agent grants and tool grants apply exactly as in the web UI. |
| ✋ | **Approvals** | A tool marked "ask first" pauses the run. In Slack this arrives as a form with Approve and Deny buttons. |

> 👥 **Two doors, one rulebook.** Slack does not bypass anything. If a person cannot use an agent or a knowledge base in the web UI, they cannot in Slack either.

---

## 2. 🧰 What you need first

This guide starts **after** the demo from the [setup guide](../docs/README.md) works in the web UI. It also assumes:

| ✔ | Already in place | Where it comes from |
| --- | --- | --- |
| ☐ | CAIPE running with docker compose, with the `rbac`, `dynamic-agents` and `rag` profiles | your CAIPE install |
| ☐ | The four agents, the `support` / `support` / `owner` teams and the Jira tool server | [Setup guide](../docs/README.md) |
| ☐ | Admin access to a Slack workspace where you may create apps | your Slack workspace |
| ☐ | Keycloak's admin console reachable, for example `http://localhost:7080/admin` through an SSH or VS Code port forward | your CAIPE install |
| ☐ | The Slack user's **email** matches a Keycloak user's email | see [3.5](#35--link-the-slack-user-to-a-keycloak-user) |

> 🔑 **Handle secrets with care.** The Slack tokens, the Keycloak client secret and the admin password all end up in `.env`. Check that it is ignored by git and has mode `600`. Never paste them into chats, tickets or screenshots.

---

## 3. 🧱 Setup, step by step

Menu names can differ a little between Slack and CAIPE versions.

### 3.1 🟣 Create the Slack app

At [api.slack.com/apps](https://api.slack.com/apps): **Create New App → From a manifest**, then pick your workspace. Or build it by hand with the settings below.

| Where in the Slack app | Set this |
| --- | --- |
| **Settings → Socket Mode** | **Enable Socket Mode**. Slack offers to generate the app-level token (next row). |
| **Settings → Basic Information → App-Level Tokens** | Generate one with the `connections:write` scope. This is the `xapp-…` token. |
| **Features → OAuth & Permissions → Bot Token Scopes** | `app_mentions:read` · `channels:history` · `channels:read` · `chat:write` · `commands` · `groups:history` · `groups:read` · `im:history` · `im:read` · `im:write` · `mpim:history` · `reactions:write` · `users:read` · `users:read.email` |
| **Features → Event Subscriptions** | Turn on **Enable Events**. Subscribe to the bot events `app_mention`, `message.channels`, `message.groups`, `message.im`. No Request URL is needed in Socket Mode. |
| **Features → Interactivity & Shortcuts** | Turn **Interactivity** on (needed for the Approve and Deny buttons). |
| **Features → App Home** | Turn on the **Messages Tab**, and tick **Allow users to send Slash commands and messages from the messages tab**. Without it, direct messages are blocked. |
| **Features → Slash Commands** *(optional)* | `/caipe-help`, `/caipe-list`, `/caipe-use`, `/caipe-effort`. Create them **after** enabling Socket Mode, and the Request URL field disappears. |
| **Settings → Install App** | **Install to Workspace**. Copy the **Bot User OAuth Token** (`xoxb-…`) from **OAuth & Permissions**. |

In Slack itself, invite the bot to the channel (`/invite @CAIPE`), and copy the channel ID: open the channel, click its name, scroll to the bottom of the **About** tab. It starts with `C`.

![Slack Bot](images/01-slack-bot.png)

---

### 3.2 🔑 Give the bot its own Keycloak identity

The bot logs in to CAIPE with the Keycloak client **`caipe-slack-bot`**. You need its secret.

1. Open the Keycloak admin console (`http://localhost:7080/admin`). Log in as `admin`.
2. Choose the **`caipe`** realm in the dropdown at the top left.
3. **Clients → `caipe-slack-bot` → Credentials** tab → copy the **Client Secret**.
   If the Credentials tab is missing, turn on **Client authentication** under **Settings** and save.

> 🔒 If you rotated the stack's default secrets, this client's secret was regenerated and is not written down anywhere. Read it from the console, or press **Regenerate**.

---

### 3.3 📝 Configure `.env`

In your CAIPE install's `.env`. Placeholders are in `<angle brackets>`.

```bash
# --- Slack tokens -------------------------------------------------------
# The bot reads the SLACK_INTEGRATION_* names. The UI's "Find channels" button
# reads the plain SLACK_BOT_TOKEN, so set both to the same values.
SLACK_INTEGRATION_BOT_TOKEN=<xoxb-...>
SLACK_INTEGRATION_APP_TOKEN=<xapp-...>
SLACK_BOT_TOKEN=<xoxb-...>
SLACK_APP_TOKEN=<xapp-...>
SLACK_INTEGRATION_BOT_MODE=socket

# --- How the bot logs in to CAIPE --------------------------------------
SLACK_INTEGRATION_ENABLE_AUTH=true
SLACK_INTEGRATION_AUTH_TOKEN_URL=http://keycloak:7080/realms/caipe/protocol/openid-connect/token
SLACK_INTEGRATION_AUTH_CLIENT_ID=caipe-slack-bot
SLACK_INTEGRATION_AUTH_CLIENT_SECRET=<client secret from 3.2>

# --- Act as the person who asked (per-user identity) --------------------
SLACK_RBAC_ENABLED=true
SLACK_WORKSPACE_ALIAS=CAIPE
KEYCLOAK_BOT_CLIENT_ID=caipe-slack-bot
KEYCLOAK_BOT_CLIENT_SECRET=<same client secret>

# --- Links, routes and the admin status check ---------------------------
CAIPE_UI_BASE_URL=https://<your-caipe-hostname>
SLACK_AGENT_ROUTES_MODE=db_prefer
SLACK_INTEGRATION_DEFAULT_AGENT_ID=<agent id for unmapped channels>
SLACK_INTEGRATION_DM_AGENT_ID=<agent id for direct messages>
SLACK_BOT_ADMIN_URL=http://slack-bot:3001
SLACK_ADMIN_JWT_ISSUER=https://<your-keycloak-hostname>/realms/caipe
```

Then add the profile to the existing line:

```bash
COMPOSE_PROFILES=<existing profiles>,slack-bot
```

| 🧩 Setting | Why it matters |
| --- | --- |
| `SLACK_INTEGRATION_ENABLE_AUTH=true` | With auth off, the bot calls the UI with no token, which an RBAC-protected UI refuses. |
| `SLACK_RBAC_ENABLED=true` + `KEYCLOAK_BOT_*` | Without it, every Slack user acts as the bot's own service account, and your team rules do not apply. With it, each request runs as the real person. |
| `SLACK_BOT_ADMIN_URL` | The UI defaults to the Kubernetes service name. In compose it must be `slack-bot:3001`, or the Slack page reports **"Degraded: Slack bot admin check timed out"**. |
| `SLACK_ADMIN_JWT_ISSUER` | Needed only if Keycloak is published under a public hostname. Tokens carry the public issuer, so the bot must expect it. |
| `SLACK_INTEGRATION_BOT_CONFIG` | Optional. A static YAML map of channel to agent. The channel routes in 3.6 are the main mechanism. |

> 🧩 **Agent IDs.** The UI may prefix agent IDs, for example `agent-support` for the agent seeded as `support`. Copy the exact ID the bot logs on the first request.

---

### 3.4 🚀 Start it

```bash
export COMPOSE_PROFILES="$(grep '^COMPOSE_PROFILES=' .env | cut -d= -f2)"
docker compose up -d slack-bot caipe-ui
docker logs -f slack-bot
```

✅ **Check:** you see `Enterprise RBAC enforcement enabled`, `Connected to CAIPE API (status 200)` and `Starting CAIPE Slack Bot in Socket Mode`.

---

### 3.5 🔗 Link the Slack user to a Keycloak user

The bot matches the **email on the Slack profile** to a Keycloak user.

| What happens | Result |
| --- | --- |
| Emails match | The bot links that Keycloak user (it stores the Slack user ID in the `slack_user_id` attribute) and calls CAIPE as them. ✅ |
| No Keycloak user matches | With `SLACK_JIT_CREATE_USER=true` (the default) the bot **creates a new user** with no roles and no teams. It works, but that person has no access to anything. ⚠️ |

So before the first message, make sure that **the email on your Slack profile is the email of the Keycloak user who has the teams you want**. Otherwise fix it afterwards:

1. In Keycloak, give the new user the roles it needs, and add it to its teams in the CAIPE web UI (**Admin → Teams**).
2. **Sign in to the CAIPE web UI once as that user.** See the note below.

> ⚠️ **One web UI sign-in is still required.** The gateway lets a user call tools only if OpenFGA holds `user:<id> caller mcp_gateway:list`, which is written on the first interactive web UI login (or by a directory sync). A user created from Slack alone does not have it, so every tool server answers **403** and the agent starts with **zero tools**. This is an open limitation.
>
> The JIT user has no password. In Keycloak, open **Users → the user → Credentials** and set one (mark it temporary), then sign in at your CAIPE URL.

---

### 3.6 🗺️ Map the channel to an agent and a team

In the CAIPE web UI, signed in as an admin: **Admin → Integrations → Slack → Onboard channels**.

1. Click **Find channels** (needs `SLACK_BOT_TOKEN` from 3.3). If it fails, paste the channel ID.
2. Select `#caipe`, then pick the **agent** (Support) and the **team** (`support`).
3. Apply.

The alternative is **Advanced → Import from Slackbot YAML**: preview, then apply. A channel imported this way still needs a team assigned.

Keep the access table of the [main README](../README.md#-who-can-reach-what) in mind. Map the channel to the team that is meant to reach that agent.

![CAIPE Slack Integration](images/02-caipe-integration-slack.png)

![CAIPE Slack Channel](images/03-caipe-slack-channel.png)

---

### 3.7 📚 Let the team search the knowledge bases

The agents use the knowledge base through the same permissions as in the web UI. For a non-admin team:

- Assign the datasources to the team (**Admin → Teams → the team**), as in the [setup guide](../docs/README.md).
- Turn on the team's **search capability**. The RAG server asks for it in addition to the per-datasource grant, so a team with a datasource but without it gets **zero results**. In OpenFGA it is the tuple `team:<slug>#member searcher organization:caipe`.

Your user passes this check through its support role, which is why it works for you in the web UI while a regular team member is refused.

---

## 4. ▶️ Run it and check it

1. In `#caipe`, send `@CAIPE hello, which tickets are open?`.
2. A plain message with no mention is ignored, since the route listens for **mentions** only.
3. Read the bot log:

```bash
docker logs --since 5m slack-bot | grep -E "invoked|mapped to team|OBO|dispatch_identity|Error"
```

| 🔎 In the log | What it tells you |
| --- | --- |
| `CAIPE was invoked by User: …, Email: <address>` | The bot sees the email. `Email: None` means `users:read.email` is missing. |
| `Channel=… mapped to team=support` | The channel route and team were found. |
| `OBO impersonation succeeded for user=<id>` | The bot is calling CAIPE as that person. |
| `dispatch_identity: run_as=obo_user agent=…` | The right agent was chosen. |

And in `dynamic-agents`:

```bash
docker logs --since 5m dynamic-agents | grep -E "loaded|MCP server|denied"
```

✅ **Healthy:** `loaded N tools from M/M MCP servers`. ❌ `HTTP 403 … [denied]` means the user cannot call tools, see [section 6](#6--when-something-goes-wrong).

![Slack questions](images/04-slack-questions.png)

# Build in cloud — Internal customer support coach in Teams using Zendesk to ch

Human-executable steps. This pack does **not** deploy to your tenant automatically.

### 0. Prerequisites
- Power Platform environment in **Europe** with Dataverse (admin.powerplatform.microsoft.com).
- Copilot Studio license / capacity; Maker role.
- Open https://copilotstudio.microsoft.com and select the EU environment.

### 1. Create agent
- Create → New agent → Name: `Internal customer support coach in Teams using Zendesk to ch`.
- Enable generative orchestration: **True** (required for MCP/CUA/multi-tool planning).
  Docs: https://learn.microsoft.com/en-us/microsoft-copilot-studio/advanced-generative-actions
- If starter fits: Employee Self-Service (IT or HR) if applicable.
  ESS: https://learn.microsoft.com/en-us/microsoft-365/copilot/employee-self-service/overview
- Write strong **descriptions** for every topic/tool/knowledge source (planner uses them).

### 1b. Capacity / licensing check
- Confirm Copilot Credits (prepaid or PAYG) — trial cannot publish.
- Estimator: https://microsoft.github.io/copilot-studio-estimator/
- Licensing: https://learn.microsoft.com/en-us/microsoft-copilot-studio/billing-licensing

### 2. Authentication
- Settings → Security → Authentication → **Authenticate with Microsoft (Entra via Teams/M365)**.
- Save and plan to **Publish** after config (auth applies on publish).
- Docs: https://learn.microsoft.com/en-us/microsoft-copilot-studio/configuration-end-user-authentication

### 3. Instructions
- Overview → Instructions: role, scope, language (FI/EN), escalate when unsure,
  never invent policy, cite knowledge, no secrets in chat.

### 4. Knowledge
- Add knowledge: **SharePoint** (Knowledge tab).
- Prefer security-trimmed SharePoint for internal content.
- Docs: https://learn.microsoft.com/en-us/microsoft-copilot-studio/knowledge-copilot-studio

### 5. Tools
- Configure: Connector actions for Microsoft Teams (see connector reference)
- Configure: Connector actions for Zendesk (see connector reference)
- Configure: Create/update ticket via ITSM connector or agent flow
- Configure: Agent flow for multi-step deterministic logic + approvals
- Prefer connector actions; use agent flows for multi-step + approvals.
- Ladder: prebuilt connector then agent flow then custom connector (OpenAPI) then HTTP then MCP then CUA.
- Convert PA cloud flow to agent flow only if in a solution; one-way billing to Copilot Studio capacity.
- Desktop flows cannot be called from agent flows (Learn FAQ).
- Connector reference: https://learn.microsoft.com/en-us/connectors/connector-reference/
- Agent flows: https://learn.microsoft.com/en-us/microsoft-copilot-studio/flows-overview
- Escalation: https://learn.microsoft.com/en-us/microsoft-copilot-studio/guidance/integrations

### 6. Topics (Tier 2+)
- Author trigger phrases for top intents; add entities (dates, ticket IDs).
- Configure Escalate system topic with human handoff path.

### 7. Channels
- Enable channel: **Microsoft Teams**
- Teams: https://learn.microsoft.com/en-us/microsoft-copilot-studio/publication-add-bot-to-microsoft-teams

### 8. Test
- Test pane: happy path, auth, tool failure, escalation, FI language sample.
- Verify citations for knowledge answers.

### 9. Publish
- Publish → required admin approvals for Teams/M365 if applicable.


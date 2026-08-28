# Integration ladder and Azure next step (official)

Never invent connector operation names. Look up https://learn.microsoft.com/en-us/connectors/connector-reference/ at design time.

Primary: https://learn.microsoft.com/en-us/microsoft-copilot-studio/guidance/integrations
Connectors in CS: https://learn.microsoft.com/en-us/microsoft-copilot-studio/advanced-connectors
Custom connectors: https://learn.microsoft.com/en-us/connectors/custom-connectors/

## Preferred order

1. **Prebuilt Power Platform connector** as agent tool (standard vs premium per plan). Optional: connectors as knowledge (preview).
2. **Agent flow** — deterministic multi-step, HITL, Key Vault / hidden secrets, convert from PA cloud flow.
3. **Custom connector** — OpenAPI or Postman wrapper around REST (Logic Apps also SOAP). Reusable. Auth: Entra, OAuth 2.0, basic, API key. From CS: Tools → New tool → Custom connector (Power Apps portal).
4. **HTTP request** in a topic — faster than a custom connector, not reusable, harder for makers.
5. **MCP** — generative orchestration required; DLP classifies MCP/connectors.
6. **Computer use** — last resort when no API. Desktop flows are **not** callable from agent flows.
7. **Bot Framework skills** — pro-code, Azure AI Bot Service, extra Azure cost, ALM outside Power Platform.

Tool credentials default to **user**. **Maker-provided** requires an authenticated channel. SSO is not supported for connectors when the agent uses custom Active Directory authentication and is deployed to Teams.

## When Copilot Studio / agent flow is too slow or limited

Official next steps in the same integration article:

- Dataverse custom APIs
- Dataverse low-code plugins
- Azure Functions

To **host** a public API for a custom connector: Azure Functions, Azure Web Apps, Azure API Apps. Private APIs: on-premises data gateway.

**Azure Logic Apps** when you need Azure-native isolation, VNet, SOAP, or consumption/standard workflow plans. A connector created in Logic Apps is **not** automatically available in PA/CS — recreate from the same OpenAPI/Postman.

Also enforce:

- Power Platform request allocations: https://learn.microsoft.com/en-us/power-platform/admin/api-request-limits-allocations
- Copilot Studio quotas: https://learn.microsoft.com/en-us/microsoft-copilot-studio/requirements-quotas (e.g. 8,000 RPM messages per agent per Dataverse environment; generative AI RPM/RPH scales with message packs; connector payload 5 MB public / 450 KB GCC)
- Per-connector limits on each connector reference page

If RPM/throttling: reduce tool chatter, batch, child flows, PAYG or more message packs, then follow Learn “Plan Copilot Studio agent deployments for throughput and rate limits”. Do not invent a quota-increase process.

## Custom connector caps (Power Automate)

50 custom connectors per user; 500 RPM per connection. Certify with Microsoft only to share with **all** CS / PA / Logic Apps users.

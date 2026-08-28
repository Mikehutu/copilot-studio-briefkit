# DLP and governance (official)

Sources:
- https://learn.microsoft.com/en-us/microsoft-copilot-studio/admin-data-loss-prevention
- https://learn.microsoft.com/en-us/microsoft-copilot-studio/security-and-governance

## Facts
- Policies in **Power Platform admin center**; real-time enforcement for makers/users.
- Connector groups: **Business / Non-business / Blocked**. Data cannot flow between different groups.
- Connectors introduced after ~2019 often land in default **Non-business** (and many orgs auto-block that group).
- **MCP** uses Power Platform connector connectivity → blocking connectors blocks MCP tools too.
- Agent DLP **exemption is not supported** (enforcement for all tenants).

## Full PPAC connector name table (Copilot Studio-specific)

| Prevent makers from… | Connector name in PPAC |
|---|---|
| App Insights telemetry | Application Insights in Copilot Studio |
| Publishing without auth | Chat without Microsoft Entra ID authentication in Copilot Studio |
| HTTP requests | HTTP (supports endpoint filtering) |
| Document knowledge | Knowledge source with documents in Copilot Studio |
| Public website knowledge | Knowledge source with public websites and data in Copilot Studio (endpoint filtering) |
| SharePoint/OneDrive knowledge | Knowledge source with SharePoint and OneDrive in Copilot Studio (endpoint filtering) |
| Direct Line / demo web / mobile | Direct Line channels in Copilot Studio |
| Dynamics 365 Customer Service channel | Omnichannel in Copilot Studio |
| Facebook | Facebook channel in Copilot Studio |
| SharePoint channel | SharePoint channel in Copilot Studio |
| Teams + Microsoft 365 channel | Microsoft Teams + Microsoft 365 Channel in Copilot Studio |
| WhatsApp | WhatsApp channel in Copilot Studio |
| Event triggers + some authenticated evals | Microsoft Copilot Studio |
| Power Platform connectors as tools | *Many prebuilt and custom connectors* (classify each) |
| Skills | Skills with Copilot Studio |

## Recommended EU enterprise baseline DLP intent
1. Block **Chat without Microsoft Entra ID authentication**
2. Place M365/Dataverse/SharePoint connectors in **Business**
3. Endpoint-filter HTTP and public websites
4. Control **Microsoft Copilot Studio** connector if autonomous triggers are restricted
5. Review Non-business default group so new connectors are not silently blocked/allowed wrongly

## Broader governance
- Disable generative AI publish tenant-wide; restrict cross-geo generative data movement
- CMK, Customer Lockbox (telemetry exclusions apply)
- Purview maker audit; Sentinel; Agent 365 identities/Conditional Access
- Environment routing; maker welcome message
- Copilot credit caps / PAYG policies
- Security scan / runtime protection status before publish

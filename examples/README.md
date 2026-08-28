# Examples — real briefs in, real solution packs out

Every folder below is a **live, generated output** of `cs-agent brief`. The brief is in
`brief.txt`; the produced solution pack (9 files) is in the named subfolder. All source
URLs were verified (HTTP 200) against Microsoft Learn at generation time.

To regenerate any example yourself:

```bash
cs-agent brief "$(cat examples/<id>/brief.txt)" --out examples/<id>
```

| # | id | Brief (summary) | Tier | Auth | Region |
|---|---|---|---|---|---|
| 1 | [ex01-it-helpdesk](ex01-it-helpdesk/) | Finnish enterprise IT helpdesk, ServiceNow tickets, Teams | Tier 2 | Entra via Teams/M365 | Europe |
| 2 | [ex02-hr-pto-workday](ex02-hr-pto-workday/) | HR PTO bot, Workday, SharePoint, FI/SV bilingual | Tier 2 | Entra via Teams/M365 | Europe |
| 3 | [ex03-multi-agent-router](ex03-multi-agent-router/) | Multi-agent router with IT/HR/finance child agents | Tier 5 | Entra via Teams/M365 | Europe |
| 4 | [ex04-autonomous-compliance-alerts](ex04-autonomous-compliance-alerts/) | Autonomous compliance agent, email trigger → ServiceNow, HITL | Tier 4 | Entra via Teams/M365 | Europe |
| 5 | [ex05-public-faq](ex05-public-faq/) | Public website customer FAQ (external) | Tier 1 | Entra/OAuth2 manually | Europe |
| 6 | [ex06-procurement-sap](ex06-procurement-sap/) | Procurement PO status + approvals, SAP, invoice/reporting | Tier 3 | Entra via Teams/M365 | Europe |
| 7 | [ex07-customer-support-zendesk](ex07-customer-support-zendesk/) | Support coach, Zendesk ticket status + email triage | Tier 3 | Entra via Teams/M365 | Europe |
| 8 | [ex08-mcp-knowledge-agent](ex08-mcp-knowledge-agent/) | MCP tools over approved server + SharePoint, EU banking | Tier 3 | Entra via Teams/M365 | Europe |
| 9 | [ex09-finance-invoice](ex09-finance-invoice/) | Finance invoice handling + approvals, Dataverse/Outlook | Tier 3 | Entra via Teams/M365 | Europe |
| 10 | [ex10-salesforce-sales](ex10-salesforce-sales/) | Sales assistant, Salesforce customer data + order status | Tier 3 | Entra via Teams/M365 | Europe |

## What each pack contains

Every generated pack has the same 9 files:

| File | What it's for |
|---|---|
| `DESIGN.md` | Tier, pattern, intent summary, architecture decisions, knowledge, tools, risks, threat model, official sources |
| `BUILD-CLOUD.md` | Ordered, human-executable steps in the Copilot Studio UI |
| `GOVERNANCE.md` | EU/FI defaults, auth, DLP connector names |
| `ALM.md` | ALM strategy + PAC CLI sketch |
| `DEPLOY.md` | Human-executed deploy runbook (Dev unmanaged → git → Test/Prod) |
| `PAC-DRY-RUN.md` | Copy-paste PAC commands (no tenant writes) |
| `CHECKLIST.md` | Go-live gate |
| `sources.json` | Every Microsoft Learn URL cited |
| `architecture.json` | Machine-readable design (tier, tools, risks, sources) |

Browse the packs to see how the same simple brief produces a complete, Learn-grounded
enterprise design with no model call and no tenant access.

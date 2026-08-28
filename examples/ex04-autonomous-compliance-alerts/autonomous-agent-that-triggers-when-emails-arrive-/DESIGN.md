# Design — Autonomous agent that triggers when emails arrive and create

**Generated:** 2026-08-28  
**Tier:** Tier 4 Autonomous/CUA  
**Pattern:** Autonomous event-driven agent


## Brief
Autonomous agent that triggers when emails arrive and creates ServiceNow tickets for compliance alerts, with human approval for high-risk actions.

## Intent summary
- Audience: internal
- Region profile: eu-fi
- Languages: en, fi
- Systems: ServiceNow
- Actions: create_or_check_ticket, approval_workflow, email_triage
- Missing fields: none flagged

## Architecture decisions
| Decision | Choice |
|---|---|
| Environment region | Europe (EU/EFTA datacenters; align tenant + environments for EU Data Boundary) |
| Authentication | Authenticate with Microsoft (Entra via Teams/M365) |
| Generative orchestration | True |
| Starter template | Employee Self-Service (IT or HR) if applicable |
| Channels | Microsoft Teams |

## Knowledge sources
- SharePoint

## Tools / actions
- Connector actions for ServiceNow (see connector reference)
- Create/update ticket via ITSM connector or agent flow
- Agent flow for multi-step deterministic logic + approvals
- Event trigger (email / Dataverse / schedule / file)
- Human-in-the-loop approval for high-risk actions

## Risks
- Autonomous actions require sandbox, logging, kill switch, DLP on triggers
- Use Dev/Test/Prod EU environments and managed solutions for production

## Threat model
- Internal-only agent. Keep Teams/M365 + Entra auth; review DLP for listed connectors.

## Official sources
- https://learn.microsoft.com/en-us/connectors/connector-reference/
- https://learn.microsoft.com/en-us/microsoft-365/copilot/employee-self-service/overview
- https://learn.microsoft.com/en-us/microsoft-copilot-studio/admin-data-loss-prevention
- https://learn.microsoft.com/en-us/microsoft-copilot-studio/configuration-end-user-authentication
- https://learn.microsoft.com/en-us/microsoft-copilot-studio/flows-faqs
- https://learn.microsoft.com/en-us/microsoft-copilot-studio/flows-overview
- https://learn.microsoft.com/en-us/microsoft-copilot-studio/guidance/alm
- https://learn.microsoft.com/en-us/microsoft-copilot-studio/guidance/autonomous-agents
- https://learn.microsoft.com/en-us/microsoft-copilot-studio/knowledge-copilot-studio
- https://learn.microsoft.com/en-us/microsoft-copilot-studio/security-and-governance
- https://learn.microsoft.com/en-us/power-platform/admin/regions-overview

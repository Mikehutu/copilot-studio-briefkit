# Design — Finnish enterprise IT helpdesk agent for employees in Teams 

**Generated:** 2026-08-28  
**Tier:** Tier 2 Self-service  
**Pattern:** Structured self-service agent


## Brief
Finnish enterprise IT helpdesk agent for employees in Teams. Password reset guidance, ServiceNow tickets, SharePoint IT docs. EU only.

## Intent summary
- Audience: internal
- Region profile: eu-fi
- Languages: en, fi
- Systems: ServiceNow, SharePoint, Microsoft Teams
- Actions: password_reset_guidance, create_or_check_ticket
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
- Connector actions for SharePoint (see connector reference)
- Connector actions for Microsoft Teams (see connector reference)
- Create/update ticket via ITSM connector or agent flow
- Guided topic for password reset (no secret storage)

## Risks
- Use Dev/Test/Prod EU environments and managed solutions for production

## Threat model
- Internal-only agent. Keep Teams/M365 + Entra auth; review DLP for listed connectors.

## Official sources
- https://learn.microsoft.com/en-us/connectors/connector-reference/
- https://learn.microsoft.com/en-us/microsoft-365/copilot/employee-self-service/overview
- https://learn.microsoft.com/en-us/microsoft-copilot-studio/admin-data-loss-prevention
- https://learn.microsoft.com/en-us/microsoft-copilot-studio/configuration-end-user-authentication
- https://learn.microsoft.com/en-us/microsoft-copilot-studio/guidance/alm
- https://learn.microsoft.com/en-us/microsoft-copilot-studio/knowledge-copilot-studio
- https://learn.microsoft.com/en-us/microsoft-copilot-studio/security-and-governance
- https://learn.microsoft.com/en-us/power-platform/admin/regions-overview

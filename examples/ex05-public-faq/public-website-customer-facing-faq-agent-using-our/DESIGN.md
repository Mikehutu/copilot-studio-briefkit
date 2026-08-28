# Design — Public website customer-facing FAQ agent using our public we

**Generated:** 2026-08-28  
**Tier:** Tier 1 Knowledge  
**Pattern:** FAQ / knowledge agent


## Brief
Public website customer-facing FAQ agent using our public website knowledge for product questions, with external authentication considerations.

## Intent summary
- Audience: external
- Region profile: eu-fi
- Languages: en, fi
- Systems: (none named — confirm)
- Actions: (knowledge only)
- Missing fields: none flagged

## Architecture decisions
| Decision | Choice |
|---|---|
| Environment region | Europe (EU/EFTA datacenters; align tenant + environments for EU Data Boundary) |
| Authentication | Authenticate manually (Entra or OAuth2) — do NOT use No authentication for personal data |
| Generative orchestration | True |
| Starter template | Custom |
| Channels | Custom website / Direct Line |

## Knowledge sources
- Public website

## Tools / actions
- None beyond generative answers

## Risks
- External channel needs explicit threat model and WAF/CDN review for Direct Line

## Threat model
- External/B2B exposure is an attack surface: Direct Line is a public endpoint.
- Rotate Direct Line secrets; put the site behind an auth layer / WAF.
- OAuth/Entra (or equivalent) before exposing; avoid no-auth for personal data.
- Rate-limit + monitor for prompt injection; review per-channel DLP connector names.
- Never embed tokens/connector credentials in the agent or repo; env vars / connection references only.

## Official sources
- https://learn.microsoft.com/en-us/microsoft-copilot-studio/configuration-end-user-authentication
- https://learn.microsoft.com/en-us/microsoft-copilot-studio/knowledge-copilot-studio
- https://learn.microsoft.com/en-us/microsoft-copilot-studio/security-and-governance
- https://learn.microsoft.com/en-us/power-platform/admin/regions-overview

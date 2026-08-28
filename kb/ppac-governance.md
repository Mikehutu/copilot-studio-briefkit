# PPAC governance — apply policies by hand (official)

Primary: https://learn.microsoft.com/en-us/power-platform/admin/admin-documentation  \nPPAC = Power Platform admin center: https://admin.powerplatform.microsoft.com

**This repo never scripts policy PUTs.** Governance is applied by a human admin
in PPAC; we document the clicks and link the official walk-throughs. A scripted
policy change requires explicit consent for that tenant — out of scope here.

## Environment (Dev/Test/Prod in Europe)
- PPAC → **Environments** → pick the **Europe**/**EU** region (aligned with your tenant's EU Data Boundary).
- Create separate **Dev / Test / Prod** environments; never co-mingle.
- Docs: https://learn.microsoft.com/en-us/power-platform/admin/create-environment
- Region/residency: https://learn.microsoft.com/en-us/microsoft-copilot-studio/geo-data-residency

## DLP policies (connector names)
- PPAC → **Data policies** → **New policy** (+ select environments).
- Add the connector **names** this pack lists (e.g. "Chat without Microsoft Entra ID authentication in Copilot Studio", "HTTP", "Microsoft Copilot Studio (triggers)", **"Azure Application Insights"**).
- Group by **Business / non-Business** to enforce: no unauthenticated chat, HTTP endpoint-filtered, MCP connector classified, App Insights allowed for telemetry.
- Docs: https://learn.microsoft.com/en-us/microsoft-copilot-studio/admin-data-loss-prevention

## Security roles / maker access
- PPAC → **Environment access** → add users by **security role** (e.g. Environment Maker / Copilot author).
- Restrict maker access to the environments that need it; use security groups for sharing published agents.
- Docs: https://learn.microsoft.com/en-us/power-platform/admin/database-security

## Copilot Hub / credit governance
- PPAC → **Copilot Hub** monitors Copilot Credits and agent usage.
- Set budgets / enforcement per policy; watch burn (see kb/observability-metrics.md).

## Click-path summary (no scripts)
1. Environments → create/verify EU Dev/Test/Prod
2. Data policies → new policy → add block/allow rules with exact connector names
3. Environment access → security roles for makers
4. Copilot Hub → credit budgets + usage review
5. (optional) App Insights → add resource + set telemetry

## Sources
- PPAC docs: https://learn.microsoft.com/en-us/power-platform/admin/admin-documentation
- DLP: https://learn.microsoft.com/en-us/microsoft-copilot-studio/admin-data-loss-prevention
- Security roles: https://learn.microsoft.com/en-us/power-platform/admin/database-security
- Create env: https://learn.microsoft.com/en-us/power-platform/admin/create-environment

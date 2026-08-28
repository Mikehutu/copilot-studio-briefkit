# Governance — Public website customer-facing FAQ agent using our public we

## Environment
- Region: Europe (EU/EFTA datacenters; align tenant + environments for EU Data Boundary)
- Recommend Dev / Test / Prod separation in EU.

## Authentication
- Authenticate manually (Entra or OAuth2) — do NOT use No authentication for personal data
- Block no-auth for internal via DLP.

## DLP recommendations (PPAC connector names)
- Chat without Microsoft Entra ID authentication in Copilot Studio → Block for internal
- HTTP → Business or endpoint-filtered
- Microsoft Copilot Studio (triggers) → control if autonomous
- Knowledge source with public websites and data in Copilot Studio → review

Official DLP: https://learn.microsoft.com/en-us/microsoft-copilot-studio/admin-data-loss-prevention  
Security overview: https://learn.microsoft.com/en-us/microsoft-copilot-studio/security-and-governance

## EU / Finland
- Align environments to Europe for EU Data Boundary.
- Languages: en, fi
- Channel copy: Finnish primary for FI employees; English fallback; Swedish if bilingual org.
- Prefer user-credential tools (SharePoint trimming).
- Not legal advice — validate with org DPO for personal data processing.

## Risks called by design
- External channel needs explicit threat model and WAF/CDN review for Direct Line

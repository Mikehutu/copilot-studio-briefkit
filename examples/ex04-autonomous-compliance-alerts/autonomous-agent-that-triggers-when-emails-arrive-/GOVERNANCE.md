# Governance — Autonomous agent that triggers when emails arrive and create

## Environment
- Region: Europe (EU/EFTA datacenters; align tenant + environments for EU Data Boundary)
- Recommend Dev / Test / Prod separation in EU.

## Authentication
- Authenticate with Microsoft (Entra via Teams/M365)
- Block no-auth for internal via DLP.

## DLP recommendations (PPAC connector names)
- Chat without Microsoft Entra ID authentication in Copilot Studio → Block for internal
- HTTP → Business or endpoint-filtered
- Microsoft Copilot Studio (triggers) → control if autonomous
- Knowledge source with SharePoint and OneDrive in Copilot Studio → Business

Official DLP: https://learn.microsoft.com/en-us/microsoft-copilot-studio/admin-data-loss-prevention  
Security overview: https://learn.microsoft.com/en-us/microsoft-copilot-studio/security-and-governance

## EU / Finland
- Align environments to Europe for EU Data Boundary.
- Languages: en, fi
- Channel copy: Finnish primary for FI employees; English fallback; Swedish if bilingual org.
- Prefer user-credential tools (SharePoint trimming).
- Not legal advice — validate with org DPO for personal data processing.

## Risks called by design
- Autonomous actions require sandbox, logging, kill switch, DLP on triggers
- Use Dev/Test/Prod EU environments and managed solutions for production

# Computer use (CUA) — official

Primary: https://learn.microsoft.com/en-us/microsoft-copilot-studio/computer-use

## What it is
Tool that lets agents operate Windows GUIs (web + desktop) via virtual mouse/keyboard when **no API** exists. Requires **generative orchestration**.

## Setup summary
1. Tools → Add tool → New tool → Computer use
2. Name, description (for planner), model, natural-language instructions
3. Optional: inputs, target machine, connection, credentials mode, human supervision, stored credentials

## Models (examples from Learn; verify current)
- OpenAI CUA — Standard — GA
- Anthropic Claude Sonnet 4.5/4.6 — Standard (admin may need external models allowed)
- Claude Opus 4.6 — Premium experimental

## Credentials
- Maker-provided (default) — caution when sharing agent (others act as maker on machine)
- End-user credentials — each user needs machine access
- Stored website/desktop credentials (internal store or Azure Key Vault)

## Human supervision
Email review path when potentially harmful instructions detected; timeout stops run if no response.

## Licensing
- Billed as agent actions; **5 Copilot Credits per step** standard models; **15** premium models.
- A single form-fill may be multiple steps (navigate, click, type, submit).

## When to use (enterprise)
- Legacy ERP UI, portals without API, swivel-chair sync
- **Last resort** after connector / custom connector / HTTP / MCP

## EU/FI notes
- Prefer Windows 365 Cloud PC / governed machine groups
- Secrets in Key Vault; no passwords in instructions
- HITL for financial/HR actions

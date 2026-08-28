# Observability, metrics & evaluation (official)

Primary: https://learn.microsoft.com/en-us/microsoft-copilot-studio/analytics-overview (analytics/Monitor)
DLP: https://learn.microsoft.com/en-us/microsoft-copilot-studio/admin-data-loss-prevention

## App Insights / analytics DLP name
- The **Azure Application Insights** connection shows in PPAC DLP as **"Azure Application Insights"** connector policy name. Use that exact name when you configure DLP rules; "Copilot Studio" analytics may surface under the same App Insights connector.
- Telemetry target: an Application Insights resource in your Azure subscription; Copilot Studio sends agent analytics there when configured.

## What to monitor
- **Credit burn** — Copilot Studio uses Copilot Credits. Watch burn vs prepaid/PAYG budget to avoid enforcement/denial. Estimator: https://microsoft.github.io/copilot-studio-estimator/
- **Session / message counts**, **escalation rate**, **error rate**, **latency**
- **Autonomous runs and CUA steps** — each bills credits; unexpected jumps = runaway loop or expensive tool chain.
- **DLP blocks** — connectors blocked by policy produce user-facing "I can't do that" style escalations; monitor support tickets for these.

## Evaluation test sets
- **Power CAT Copilot Studio Kit**: https://github.com/microsoft/Power-CAT-Copilot-Studio-Kit — scripted UI test harness for Copilot Studio agents. Run a golden utterance set before every prod release.
- **Direct Line**: automated smoke tests against a Direct Line endpoint for core utterances — catch regressions without a human in the test pane.
- **Golden packs** in this repo (`tests/goldens/briefs.json`) are the design-time eval set — they verify the *designer*, not the deployed bot.

## Design implication
Every enterprise pack should: (1) cite the App Insights DLP name, (2) record a credit estimate, (3) define an evaluation test set before prod. Note: **we do not provision App Insights for a tenant** — we tell the maker how, with the exact DLP name.

## Sources
- Analytics overview: https://learn.microsoft.com/en-us/microsoft-copilot-studio/analytics-overview
- DLP (App Insights name): https://learn.microsoft.com/en-us/microsoft-copilot-studio/admin-data-loss-prevention
- Credit estimator: https://microsoft.github.io/copilot-studio-estimator/
- Power CAT Kit: https://github.com/microsoft/Power-CAT-Copilot-Studio-Kit

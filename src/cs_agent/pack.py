"""Write Solution Pack markdown artifacts."""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path

from .models import Architecture


def _today() -> str:
    return datetime.now(UTC).date().isoformat()


def write_pack(arch: Architecture, out_dir: Path) -> Path:
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    slug = _slug(arch.intent.name)
    pack = out_dir / slug
    pack.mkdir(parents=True, exist_ok=True)

    (pack / "DESIGN.md").write_text(_design_md(arch), encoding="utf-8")
    (pack / "BUILD-CLOUD.md").write_text(_build_md(arch), encoding="utf-8")
    (pack / "GOVERNANCE.md").write_text(_gov_md(arch), encoding="utf-8")
    (pack / "ALM.md").write_text(_alm_md(arch), encoding="utf-8")
    (pack / "DEPLOY.md").write_text(_deploy_md(arch), encoding="utf-8")
    (pack / "PAC-DRY-RUN.md").write_text(_pac_md(arch), encoding="utf-8")
    (pack / "CHECKLIST.md").write_text(_checklist_md(arch), encoding="utf-8")
    (pack / "sources.json").write_text(
        json.dumps({"sources": arch.sources, "generated": _today()}, indent=2),
        encoding="utf-8",
    )
    (pack / "architecture.json").write_text(json.dumps(arch.to_dict(), indent=2), encoding="utf-8")
    return pack


def _slug(name: str) -> str:
    s = "".join(c if c.isalnum() or c in "-_" else "-" for c in name.lower()).strip("-")
    return s[:50] or "solution-pack"


def _design_md(a: Architecture) -> str:
    i = a.intent
    return f"""# Design — {i.name}

**Generated:** {_today()}  
**Tier:** {a.tier_label}  
**Pattern:** {a.pattern}


## Brief
{i.raw_brief}

## Intent summary
- Audience: {i.audience}
- Region profile: {i.region}
- Languages: {", ".join(i.languages)}
- Systems: {", ".join(i.systems) or "(none named — confirm)"}
- Actions: {", ".join(i.actions) or "(knowledge only)"}
- Missing fields: {", ".join(i.missing) or "none flagged"}

## Architecture decisions
| Decision | Choice |
|---|---|
| Environment region | {a.environment_region} |
| Authentication | {a.auth} |
| Generative orchestration | {a.generative_orchestration} |
| Starter template | {a.starter_template or "Custom"} |
| Channels | {", ".join(a.channels)} |

## Knowledge sources
{chr(10).join(f"- {k}" for k in a.knowledge)}

## Tools / actions
{chr(10).join(f"- {t}" for t in a.tools)}

## Risks
{chr(10).join(f"- {r}" for r in a.risks) or "- (none extra)"}

## Threat model
{_threat_section(a)}

## Official sources
{chr(10).join(f"- {s}" for s in a.sources)}
"""


def _threat_section(a: Architecture) -> str:
    """Threat-model notes; only non-internal (public/B2B/mixed) agents get a full section."""
    if a.intent.audience == "internal":
        return "- Internal-only agent. Keep Teams/M365 + Entra auth; review DLP for listed connectors."
    lines = [
        "- External/B2B exposure is an attack surface: Direct Line is a public endpoint.",
        "- Rotate Direct Line secrets; put the site behind an auth layer / WAF.",
        "- OAuth/Entra (or equivalent) before exposing; avoid no-auth for personal data.",
        "- Rate-limit + monitor for prompt injection; review per-channel DLP connector names.",
        "- Never embed tokens/connector credentials in the agent or repo; env vars / connection references only.",
    ]
    return chr(10).join(f"- {l}" if not l.startswith("- ") else l for l in lines)


def _build_md(a: Architecture) -> str:
    steps = [
        "### 0. Prerequisites",
        "- Power Platform environment in **Europe** with Dataverse (admin.powerplatform.microsoft.com).",
        "- Copilot Studio license / capacity; Maker role.",
        "- Open https://copilotstudio.microsoft.com and select the EU environment.",
        "",
        "### 1. Create agent",
        f"- Create → New agent → Name: `{a.intent.name}`.",
        f"- Enable generative orchestration: **{a.generative_orchestration}** (required for MCP/CUA/multi-tool planning).",
        "  Docs: https://learn.microsoft.com/en-us/microsoft-copilot-studio/advanced-generative-actions",
        f"- If starter fits: {a.starter_template or 'skip templates; blank agent'}.",
        "  ESS: https://learn.microsoft.com/en-us/microsoft-365-copilot/extensibility/employee-self-service-agent",
        "- Write strong **descriptions** for every topic/tool/knowledge source (planner uses them).",
        "",
        "### 1b. Capacity / licensing check",
        "- Confirm Copilot Credits (prepaid or PAYG) — trial cannot publish.",
        "- Estimator: https://microsoft.github.io/copilot-studio-estimator/",
        "- Licensing: https://learn.microsoft.com/en-us/microsoft-copilot-studio/billing-licensing",
        "",
        "### 2. Authentication",
        f"- Settings → Security → Authentication → **{a.auth}**.",
        "- Save and plan to **Publish** after config (auth applies on publish).",
        "- Docs: https://learn.microsoft.com/en-us/microsoft-copilot-studio/configuration-end-user-authentication",
        "",
        "### 3. Instructions",
        "- Overview → Instructions: role, scope, language (FI/EN), escalate when unsure,",
        "  never invent policy, cite knowledge, no secrets in chat.",
        "",
        "### 4. Knowledge",
    ]
    for k in a.knowledge:
        steps.append(f"- Add knowledge: **{k}** (Knowledge tab).")
    steps += [
        "- Prefer security-trimmed SharePoint for internal content.",
        "- Docs: https://learn.microsoft.com/en-us/microsoft-copilot-studio/knowledge-copilot-studio",
        "",
        "### 5. Tools",
    ]
    for t in a.tools:
        steps.append(f"- Configure: {t}")
    steps += [
        "- Prefer connector actions; use agent flows for multi-step + approvals.",
        "- Ladder: prebuilt connector then agent flow then custom connector (OpenAPI) then HTTP then MCP then CUA.",
        "- Convert PA cloud flow to agent flow only if in a solution; one-way billing to Copilot Studio capacity.",
        "- Desktop flows cannot be called from agent flows (Learn FAQ).",
        "- Connector reference: https://learn.microsoft.com/en-us/connectors/connector-reference/",
        "- Agent flows: https://learn.microsoft.com/en-us/microsoft-copilot-studio/flows-overview",
        "- Escalation: https://learn.microsoft.com/en-us/microsoft-copilot-studio/guidance/integrations",
        "",
        "### 6. Topics (Tier 2+)",
        "- Author trigger phrases for top intents; add entities (dates, ticket IDs).",
        "- Configure Escalate system topic with human handoff path.",
        "",
        "### 7. Channels",
    ]
    for c in a.channels:
        steps.append(f"- Enable channel: **{c}**")
    steps += [
        "- Teams: https://learn.microsoft.com/en-us/microsoft-copilot-studio/publication-add-bot-to-microsoft-teams",
        "",
        "### 8. Test",
        "- Test pane: happy path, auth, tool failure, escalation, FI language sample.",
        "- Verify citations for knowledge answers.",
        "",
        "### 9. Publish",
        "- Publish → required admin approvals for Teams/M365 if applicable.",
        "",
    ]
    if a.tier >= 4:
        steps += [
            "### 10. Autonomous / CUA extras",
            "- Add triggers only after DLP review.",
            "- Autonomous: https://learn.microsoft.com/en-us/microsoft-copilot-studio/autonomous-agents",
            "- Computer use last resort: https://learn.microsoft.com/en-us/microsoft-copilot-studio/computer-use",
            "- Require HITL for high-risk actions.",
            "",
        ]
    if a.tier >= 5:
        steps += [
            "### 11. Multi-agent",
            "- Build child agents first; connect from router.",
            "- https://learn.microsoft.com/en-us/microsoft-copilot-studio/connected-agents",
            "",
        ]
    return f"""# Build in cloud — {a.intent.name}

Human-executable steps. This pack does **not** deploy to your tenant automatically.

{chr(10).join(steps)}
"""


def _gov_md(a: Architecture) -> str:
    return f"""# Governance — {a.intent.name}

## Environment
- Region: {a.environment_region}
- Recommend Dev / Test / Prod separation in EU.

## Authentication
- {a.auth}
- Block no-auth for internal via DLP.

## DLP recommendations (PPAC connector names)
{chr(10).join(f"- {d}" for d in a.dlp_connectors)}

Official DLP: https://learn.microsoft.com/en-us/microsoft-copilot-studio/admin-data-loss-prevention  
Security overview: https://learn.microsoft.com/en-us/microsoft-copilot-studio/security-and-governance

## EU / Finland
- Align environments to Europe for EU Data Boundary.
- Languages: {", ".join(a.intent.languages)}
- Channel copy: Finnish primary for FI employees; English fallback; Swedish if bilingual org.
- Prefer user-credential tools (SharePoint trimming).
- Not legal advice — validate with org DPO for personal data processing.

## Risks called by design
{chr(10).join(f"- {r}" for r in a.risks) or "- None extra"}
"""


def _alm_md(a: Architecture) -> str:
    return f"""# ALM — {a.intent.name}

## Solution strategy
1. Create unmanaged solution in **Dev** (EU).
2. Add agent + connection references + env variables.
3. Export unmanaged for source control (`pac solution unpack`).
4. Export **managed** for Test/Prod import.

## PAC CLI sketch
```bash
pac auth create --environment "https://<dev>.crm4.dynamics.com"
pac solution export --name "<Solution>" --path ./exports/sol.zip --managed false
pac solution unpack --zipfile ./exports/sol.zip --folder ./src/solution
# after review
pac solution export --name "<Solution>" --path ./exports/sol_managed.zip --managed true
pac auth create --environment "https://<test>.crm4.dynamics.com"
pac solution import --path ./exports/sol_managed.zip --force-overwrite
```

Docs: https://learn.microsoft.com/en-us/power-platform/developer/cli/introduction  
ALM: https://learn.microsoft.com/en-us/microsoft-copilot-studio/guidance/alm

## Testing
- Power CAT Copilot Studio Kit: https://github.com/microsoft/Power-CAT-Copilot-Studio-Kit
- Direct Line automated tests for core utterances
- Evaluation test sets before prod

## Dry-run CLI
```bash
cs-agent pac plan
# never: cs-agent pac plan --execute  (blocked without --i-confirm-yes; writes still refused)
```

## Tier note
Delivery tier for this design: **{a.tier_label}** — ALM mandatory for production at Tier 2+.
"""


def _pac_md(a: Architecture) -> str:
    from .pac import plan_alm

    plan = plan_alm()
    cmds = "\n".join(f"  {c}" for c in plan.commands)
    notes = "\n".join(f"- {n}" for n in plan.notes)
    return f"""# PAC dry-run — {a.intent.name}

{notes}

```bash
{cmds}
```

Docs: https://learn.microsoft.com/en-us/power-platform/developer/cli/introduction
"""


def _checklist_md(a: Architecture) -> str:
    return f"""# Go-live checklist — {a.intent.name}

- [ ] EU environment region confirmed
- [ ] Auth configured and tested ({a.auth})
- [ ] Knowledge sources correct and security-trimmed
- [ ] Tools use least privilege / user credentials where possible
- [ ] DLP reviewed for listed connectors
- [ ] Escalation path tested
- [ ] Channels approved (Teams admin if needed)
- [ ] Analytics / App Insights configured as policy requires (see DEPLOY.md)
- [ ] Monitoring alerting (credit burn, errors, latency) reviewed
- [ ] Evaluation test sets run before prod (Power CAT Copilot Studio Kit)
- [ ] Managed solution import path to Test/Prod documented (DEPLOY.md)
- [ ] Support owners trained on handoff
- [ ] Credit/capacity estimate recorded
- [ ] Missing brief fields resolved: {", ".join(a.intent.missing) or "n/a"}
"""


def _deploy_md(a: Architecture) -> str:
    return f"""# Deployment / ALM runbook — {a.intent.name}

**Human-executed, no silent import.** Every command here is a step a human runs
after printed pre-flight and tenant consent. PAC never mutates a tenant from this
repo or CLI automatically.

## Pipeline

1. **Dev** (Europe env) — build and test the agent in the unmanaged solution.
2. **Export unmanaged** → unpack to git for review + source control.
3. **Export managed** → import to **Test**, validate, then **Prod**.
4. Connection references + environment variables keep endpoints/secrets out of the zip.

## PAC sequence (copy-paste after your OWN `pac auth`)

```bash
# 1. Dev export (unmanaged) → source control
pac solution export --name "<Solution>" --path ./exports/sol_dev.zip --managed false
pac solution unpack --zipfile ./exports/sol_dev.zip --folder ./src/solution
git add ./src/solution && git commit -m "solution unpack: <Solution>"

# 2. Managed import → Test
pac solution export --name "<Solution>" --path ./exports/sol_test.zip --managed true
pac auth create --environment "https://<test>.crm4.dynamics.com"
pac solution import --path ./exports/sol_test.zip --force-overwrite

# 3. Managed import → Prod (after Test sign-off + printed pre-flight)
pac auth create --environment "https://<prod>.crm4.dynamics.com"
pac solution import --path ./exports/sol_prod.zip --force-overwrite
```

> Replace `<Solution>`, `<test>`, `<prod>` with real names. Secrets are env vars /
> connection reference names, never literals in this file.

## Connection references / env vars

- Name each external endpoint as an **environment variable** (e.g. `SERVICENOW_URL`)
- Store connector credentials as **connection references** (not in code/packs)
- Rotation = update the reference; no redeploy

## Verification gates (no silent skip)

- [ ] Dev unmanaged exports cleanly + unpacks to git
- [ ] Test import succeeds; agent answers a smoke utterance with EU region
- [ ] Prod import succeeds only after Test green + explicit approval
- [ ] No secrets in commit; `pac org list` shows Europe envs (use `cs-agent pac status`)

## ALM docs
- https://learn.microsoft.com/en-us/microsoft-copilot-studio/guidance/alm
- https://learn.microsoft.com/en-us/power-platform/developer/cli/introduction
- Power CAT Copilot Studio Kit: https://github.com/microsoft/Power-CAT-Copilot-Studio-Kit
"""

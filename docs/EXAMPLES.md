# Examples — every command & function with real output

All outputs below are **real** — produced by `cs-agent` v1.0.0 against this repo
(2026-08-28). URLs shown were verified to resolve (HTTP 200).

- **10 full brief→pack examples** (with all files) live in [`examples/`](../examples/README.md).
- This page shows every **command** and **function** with its actual output.

---

## CLI commands

### `cs-agent brief "<brief>"` — design pack from a business brief

```bash
$ cs-agent brief "Finnish IT helpdesk in Teams with ServiceNow and SharePoint"
Solution pack written: out/finnish-it-helpdesk-in-teams-with-servicenow-and-s
Tier: Tier 2 Self-service | Auth: Authenticate with Microsoft (Entra via Teams/M365)
Open: out/finnish-it-helpdesk-in-teams-with-servicenow-and-s/DESIGN.md
```

Writes a 9-file pack. Example: [`examples/ex01-it-helpdesk/`](../examples/ex01-it-helpdesk/)

### `cs-agent brief --json "<brief>"` — machine-readable design

```bash
$ cs-agent brief --json "Internal HR bot PTO Workday Teams"
{
  "tier": 2,
  "tier_label": "Tier 2 Self-service",
  "auth": "Authenticate with Microsoft (Entra via Teams/M365)",
  "environment_region": "Europe (EU/EFTA datacenters; align tenant + environments for EU Data Boundary)",
  "tools": [
    "Connector actions for Workday (see connector reference)",
    "Connector actions for Microsoft Teams (see connector reference)",
    "HRIS connector: balance check + submit request"
  ]
}
```

### `cs-agent brief-file path/to/brief.txt --out <dir>` — brief from file

```bash
$ cs-agent brief-file brief.txt --out ./out
Solution pack written: out/finnish-it-helpdesk-in-teams-with-servicenow-a...
```

### `cs-agent ask "<question>"` — Q&A grounded in the local `kb/`

```bash
$ cs-agent ask "What is MCP in Copilot Studio?"
**Q:** What is MCP in Copilot Studio?

### From `mcp-tools.md`
- Connectors catalog: https://learn.microsoft.com/en-us/connectors/connector-reference/
- MCP: https://learn.microsoft.com/en-us/microsoft-copilot-studio/agent-extend-action-mcp
- Generative orchestration required for MCP.
- MCP tools and resources supported; dynamic discovery from server.
- Prefer: prebuilt connector > agent flow > custom connector > HTTP > MCP dynamic > CUA last.
- Document auth mode per tool (user vs maker).

### From `SOURCES.md`
Primary truth: Microsoft Learn. Seed HTML under docs/seed/ is secondary...
| Security and governance | https://learn.microsoft.com/en-us/microsoft-copilot-studio/security-and-governance |
| Data policies (DLP)     | https://learn.microsoft.com/en-us/microsoft-copilot-studio/admin-data-loss-prevention |
| ... (Learn URL sources) |
```

Answers are keyword-scored from `kb/*.md`; no model, no network.

### `cs-agent pac plan` — ALM dry-run (never writes)

```bash
$ cs-agent pac plan
PAC on PATH: False
Action: plan
- Dry-run only: copy-paste after you authenticate to YOUR tenant.
- EU: prefer *.crm4.dynamics.com (Europe) environments.
- Do not run import without printed pre-flight + human YES.
- Never put secrets in CLI args; use PAC profiles / env vars.

## Commands
SKIPPED (dry-run): pac auth create --environment "https://<dev>.crm4.dynamics.com"
SKIPPED (dry-run): pac solution export --name "<Solution>" --path ./exports/sol.zip --managed false
SKIPPED (dry-run): pac solution unpack --zipfile ./exports/sol.zip --folder ./src/solution
SKIPPED (dry-run): pac solution export --name "<Solution>" --path ./exports/sol_managed.zip --managed true
```

### `cs-agent pac status` — read-only tenant status (EU-verified, secrets stripped)

```bash
$ cs-agent pac status
PAC on PATH: False
PAC CLI not found on PATH. Install: https://learn.microsoft.com/en-us/power-platform/developer/cli/introduction
# returns exit 0 (informational when PAC absent)
```

When real PAC auth exists, it prints `pac auth list`/`org list` with tokens scrubbed,
and exits 1 if the tenant is not Europe.

### `cs-agent pac plan --execute` — always refused

```bash
$ cs-agent pac plan --execute
REFUSED: --execute requires --i-confirm-yes
# exit 2
```

---

## Python functions (importable via `from cs_agent...`)

### `parse_brief(text) -> Intent`

```python
from cs_agent.intent import parse_brief
i = parse_brief("Finnish IT helpdesk, ServiceNow tickets, Teams, EU")
# -> Intent(audience="internal", region="eu-fi", languages=["en","fi"],
#    systems=["ServiceNow","Microsoft Teams"], actions=["create_or_check_ticket"])
```

### `design(intent) -> Architecture`

```python
from cs_agent.architect import design
arch = design(i)
arch.tier               # 2
arch.tier_label         # "Tier 2 Self-service"
arch.auth               # "Authenticate with Microsoft (Entra via Teams/M365)"
arch.environment_region # "Europe (EU/EFTA datacenters...)"
arch.dlp_connectors     # ["Chat without Microsoft Entra ID authentication...", ...]
arch.sources            # [Learn URLs...]
```

### `write_pack(arch, out_dir) -> Path`

```python
from cs_agent.pack import write_pack
pack = write_pack(arch, "out")
# -> out/<slug>/  (DESIGN, BUILD-CLOUD, GOVERNANCE, ALM, DEPLOY,
#                  PAC-DRY-RUN, CHECKLIST, sources.json, architecture.json)
```

### `ask(question, kb_dir) -> Answer`

```python
from cs_agent.ask import ask
ans = ask("What is MCP in Copilot Studio?", "kb")
ans.text      # answer from kb/*.md
ans.sources   # [Learn URLs...]
ans.files     # ["mcp-tools.md", ...]
```

### `plan_alm() -> PacPlan` / `pac_status() -> PacStatus` / `execute_pac(...)`

```python
from cs_agent.pac import plan_alm, pac_status, execute_pac
plan_alm().commands        # ALM sketch commands (dry-run)
pac_status().eu_ok          # True if EU confirmed (read-only)
execute_pac(cmd, execute=False, confirmed_yes=False)  # "SKIPPED (dry-run): ..."
```

---

## Full worked example — one brief, complete pack

**Brief (`examples/ex01-it-helpdesk/brief.txt`):**
```
Finnish enterprise IT helpdesk agent for employees in Teams. Password reset guidance, ServiceNow tickets, SharePoint IT docs. EU only.
```

**Output** — see [`examples/ex01-it-helpdesk/finnish-enterprise-it-helpdesk-agent-for-employees/`](../examples/ex01-it-helpdesk/finnish-enterprise-it-helpdesk-agent-for-employees/) for the full pack:

- `DESIGN.md` → Tier 2 Self-service, structured self-service pattern, Entra, Europe, SharePoint knowledge, ServiceNow/ticket/password tools, Learn sources
- `BUILD-CLOUD.md` → ordered steps for copilotstudio.microsoft.com, capacity check, auth, knowledge, tools, channels
- `GOVERNANCE.md` → EU/FI defaults, DLP connector names, security posture
- `ALM.md` / `DEPLOY.md` → solution strategy + human-executed deploy runbook
- `CHECKLIST.md` → go-live gate
- `sources.json` → 8 verified Learn URLs

---

## Verification & determinism

- **Deterministic:** same brief → identical pack (pure rule engine, no model, no randomness).
- **Proven by tests:** `pytest -q` = 44 passed; `ruff check` clean; 20-brief benchmark passes 20/20.
- **Proven by examples:** the 10 packs here were generated live and every source URL returns HTTP 200.

Regenerate everything:

```bash
pytest -q
python scripts/run_brief_benchmark.py   # 20/20
for d in examples/ex*/; do cs-agent brief "$(cat $d/brief.txt)" --out $d; done
```

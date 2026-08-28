<p align="center">
  <img src="assets/logo.png" alt="copilot-studio-briefkit logo" width="140">
</p>

# Copilot Studio Briefkit

**`cs-agent`** — a **design-first CLI** that turns a business brief into an enterprise **solution pack** for [Microsoft Copilot Studio](https://learn.microsoft.com/en-us/microsoft-copilot-studio/) — architecture, governance, cloud build steps, ALM, and Learn citations.

It is **not** Copilot Studio itself, not a bot runtime, and **not** a tenant publisher. You (or a maker) still build in `copilotstudio.microsoft.com`. This tool stops the usual failure mode: unauthenticated agents, wrong region, invented connectors, and no DLP plan.

Defaults are **EU/Finland enterprise**: Europe environments, Entra auth, DLP-aware connector names from Learn, Teams-first internal, lowest viable tier.

Not affiliated with Microsoft. Use with your org's licensing.

---

## Who it is for

| Who | What they get |
|---|---|
| **CoE / security (EU/FI)** | Packs that default Entra + Europe + official PPAC DLP names, so reviews start from a defensible baseline |
| **Solution architects / SIs** | Tier (knowledge → tools → agent flows → autonomous/CUA → multi-agent), systems map, SOW-ready DESIGN + risks |
| **Makers / consultants** | Ordered `BUILD-CLOUD.md` for the Copilot Studio UI, plus PAC sketches they can copy — no guessing |
| **Coding agents / CI** | Deterministic CLI + tests + benchmark — point your own agents at any OpenAI-compatible model (see [docs/PROVIDERS.md](docs/PROVIDERS.md)) |

If you need a live bot in a customer tenant, this repo only **guides** that work. Live PAC import needs your PAC login and an explicit YES.

---

## What it is (and is not)

**Is**

- Brief → intent → architecture → folder of markdown + `sources.json`
- Q&A over a local `kb/` grounded in Microsoft Learn (agent flows vs Power Automate, custom connectors, MCP, DLP, EUDB, quotas)
- Integration **ladder**: prebuilt connector → agent flow → custom connector (OpenAPI) → HTTP → MCP → computer use last → Azure Functions / Logic Apps / Dataverse when limits hit
- PAC **dry-run** (`cs-agent pac plan`) + read-only **status** (`cs-agent pac status`)
- **Deterministic and model-free** — no API keys, no network, no LLM calls to generate packs

**Is not**

- A replacement for Learn or the 1,400+ connector schemas (look up operations on the [connector reference](https://learn.microsoft.com/en-us/connectors/connector-reference/) at design time)
- Automatic publish, DLP apply, or App Insights provisioning
- Legal advice (GDPR / EU Data Boundary — point to Trust Center / DPO)

---

## Quickstart

Python 3.11+.

```bash
git clone https://github.com/Mikehutu/copilot-studio-briefkit.git
cd copilot-studio-briefkit
python3 -m venv .venv && . .venv/bin/activate
pip install -e ".[dev]"
pytest -q
```

### 1. Design from a brief (main job)

```bash
cs-agent brief "Finnish IT helpdesk in Teams with ServiceNow and SharePoint"
```

Writes `out/<slug>/`:

| File | Use |
|---|---|
| `DESIGN.md` | Tier, auth, knowledge, tools, risks, threat model |
| `GOVERNANCE.md` | EU/FI, DLP connector names |
| `BUILD-CLOUD.md` | Ordered UI steps in Copilot Studio |
| `ALM.md` / `DEPLOY.md` / `PAC-DRY-RUN.md` | ALM + human-executed deploy runbook + PAC copy-paste (no secrets) |
| `CHECKLIST.md` | Go-live gate |
| `sources.json` | Learn URLs used |

JSON only (no files):

```bash
cs-agent brief --json "HR PTO Workday Teams Finland"
cs-agent brief-file path/to/brief.txt --out ./out
```

### 2. Ask official-doc questions

```bash
cs-agent ask "How are agent flows different from Power Automate cloud flows?"
cs-agent ask "How does DLP apply to MCP?"
```

Answers come from `kb/` plus Learn URLs. If the kb has no match, it points at Learn and **does not invent** product behavior.

### 3. PAC sketches (no tenant)

```bash
cs-agent pac plan      # dry-run ALM sketch
cs-agent pac status    # read-only: PAC on PATH, EU region, secrets stripped
```

`--execute` is refused without `--i-confirm-yes`, and **writes are still blocked** in this build. `pac status` never writes; non-EU tenants exit 1; PAC absent exits 0 (informational).

### 4. Deployment / ALM runbook

Every pack includes **`DEPLOY.md`**: Dev unmanaged → unpack to git → managed import Test/Prod, connection references, env vars. Human-executed — no silent import.

### 5. Test agents with local mocks (aimock)

`aimock/` ships a deterministic mock server for testing anything the AI stack talks to — LLM APIs now, MCP/A2A/vector next — with no keys and no network:

```bash
npm install -g @copilotkit/aimock
aimock -c aimock/aimock.json -p 4010 &          # mock server on :4010
python -m pytest tests/test_aimock.py -v        # determinism gate (skips without Node)
```

Point a client at `http://127.0.0.1:4010/v1` with a dummy key for scripted, repeatable replies. See `aimock/README.md`.

### 6. Use it with any OpenAI-compatible model

The engine is model-free, but if you want VS Code Copilot, aimock recording, or your own agents to talk to a model (local vLLM/Ollama, GitHub Models, Azure OpenAI, AI Foundry), see **[docs/PROVIDERS.md](docs/PROVIDERS.md)** — full base-URL + key + config recipes.

---

## Defaults baked into every pack

- Environment: Europe / EU Data Boundary alignment
- Auth: Entra (never "no authentication" for internal employees)
- Tools: name the **pattern** (connector / agent flow / custom connector); do not invent operation IDs
- Languages: FI/EN (SV if the brief says Swedish)
- Secrets: env-var **names** only

---

## Project layout

```
src/cs_agent/     CLI + brief→pack engine (zero runtime deps)
tests/            pytest (no live tenant)
kb/               Learn-grounded notes (SOURCES.md is the index)
aimock/           deterministic mock server + fixtures
scripts/          benchmark harness
docs/PROVIDERS.md provider wiring guide
.github/workflows/ci.yml
```

## Verify / CI

Local: `pytest -q && ruff check src tests`

GitHub Actions on `main` (push/PR): ruff, pytest, aimock probe, 20-brief benchmark. No secrets, no PAC, no external model calls.

## More

- [CHANGELOG.md](CHANGELOG.md) — version history
- [docs/EXAMPLES.md](docs/EXAMPLES.md) — every command & function with real output
- [examples/](examples/README.md) — 10 real briefs → complete solution packs
- [docs/PROVIDERS.md](docs/PROVIDERS.md) — local + Microsoft provider wiring
- [kb/SOURCES.md](kb/SOURCES.md) — official URLs the packs cite (all HTTP-verified by CI)

## License

MIT. Use with your organization's Microsoft licensing.

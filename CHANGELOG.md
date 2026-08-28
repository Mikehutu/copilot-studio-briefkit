# Changelog

All notable changes to cs-agent.

## [1.0.0] - 2026-08-28

Initial public release. Clean, self-contained repo (MIT). Product-ready.

### Added
- PAC read-only status: `cs-agent pac status` detects PAC on PATH, reads `pac auth list`/`org list`, strips tokens/secrets, infers EU region, blocks (exit 1) non-EU tenants.
- Deployment/ALM runbook: every pack emits `DEPLOY.md` (Dev unmanaged → unpack to git → managed import Test/Prod). Human-executed, no silent import.
- Metrics & evaluation: `kb/observability-metrics.md` (App Insights DLP name, credit estimator, Power CAT Copilot Studio Kit); CHECKLIST covers App Insights / monitoring / eval sets.
- PPAC governance guide: `kb/ppac-governance.md` (admin-click docs; no scripted policy PUT).
- Channel-publish guidance: threat-model + Direct Line secrets in `kb/channels-publishing.md`; public/B2B packs get a threat-model section.
- Provider wiring guide: [docs/PROVIDERS.md](docs/PROVIDERS.md) + `.env.example` for OpenAI-compatible consumers (local vLLM/Ollama, GitHub Models, Azure OpenAI, Azure AI Foundry).

### Changed
- `cs-agent pac plan` stays dry-run only; writes remain blocked.
- CI: ruff, pytest (3.11/3.12), aimock probe, 20-brief benchmark. No secrets, no PAC, no external model calls.

## [0.7.0] - 2026-08-28

- PAC read-only status (`cs-agent pac status`): detects PAC, runs `auth list`/`org list`, scrubs secrets, blocks non-EU (exit 1), informational exit 0 when PAC absent.
- `DEPLOY.md` emitted in every pack (human-executed ALM runbook).
- `kb/observability-metrics.md`, `kb/ppac-governance.md`, threat-model section for public/B2B packs.
- 44 tests, ruff clean, benchmark 20/20.

## [0.6.0] - 2026-08-28

- aimock dev-mock harness: local deterministic mock server (LLM + MCP/A2A/vector stanzas) for testing agents before tenant work.
- Determinism gate `tests/test_aimock.py` (skips without Node; CI stays green).
- Record & replay: `llmock --record` against any local OpenAI-compatible endpoint → committed fixture → offline deterministic replay.
- PyRIT red-team guide (`docs/pyrit-redteam.md`) — offense counterpart to aimock; consent-gated, own/client-authorized targets only.
- No runtime deps added (CS agent stays zero-dep).

## [0.5.1] - 2026-08-27

- Spec alignment for v0.5 product state.

## [0.5.0] - 2026-08-27

- Agent flows vs Power Automate, custom connectors, CS/PA limits, Azure escalation in `kb/` + pack ladder.
- Never invent connector operations.

## [0.4.2] - 2026-08-27

- GitHub Actions CI (ruff, pytest, DOX, 20-brief benchmark); no PAC in CI.
- Public FAQ no longer implies SharePoint; `approved` ≠ `reporting`; MCP briefs → tier 3.

## [0.4.1] - 2026-08-27

- PAC dry-run: `cs-agent pac plan`; writes refused even with `--execute --i-confirm-yes`.
- Pack emits `PAC-DRY-RUN.md`; FI language notes in GOVERNANCE.

## [0.4.0] - 2026-08-27

- Golden briefs: HR PTO, autonomous email, multi-agent router, public FAQ.
- `tests/goldens/briefs.json` + key-section snapshot tests.

## [0.3.0] - 2026-08-13

- DOX structure: root AGENTS.md + child AGENTS.md; `scripts/sdd-dox-check` + `sdd-validate`.

## [0.2.0] - 2026-08-12

- Expanded official KB: channels/publishing, licensing/credits, generative orchestration, computer use, connector patterns.
- Full PPAC DLP connector name table from Learn; EUDB rule.
- BUILD-CLOUD adds orchestration + credit check steps.

## [0.1.0] - 2026-08-12

- Initial SDD project via sdd-kit.
- Official kb (auth, DLP, MCP, knowledge, EU/FI, ALM, tiers, sources).
- Brief → intent → architecture → solution pack engine.
- CLI: `cs-agent ask | brief | brief-file`.
- Tests for EU defaults, pack artifacts, KB ask.

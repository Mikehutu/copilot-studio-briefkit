"""Run 20 golden briefs through cs-agent; deterministic PRD gates. No live PAC."""

from __future__ import annotations

import json
import re
from pathlib import Path

from cs_agent.architect import design
from cs_agent.intent import parse_brief
from cs_agent.pack import write_pack

ROOT = Path(__file__).resolve().parents[1]
BRIEFS = ROOT / "docs" / "benchmark" / "briefs-20.json"
OUT = ROOT / "docs" / "benchmark" / "packs"
SOURCES = ROOT / "kb" / "SOURCES.md"


def _learn_urls() -> set[str]:
    return set(re.findall(r"https://learn\.microsoft\.com[^\s|]+", SOURCES.read_text(encoding="utf-8")))


def score_pack(arch, pack: Path, learn: set[str]) -> dict:
    files = {p.name for p in pack.iterdir() if p.is_file()}
    required = {
        "DESIGN.md",
        "BUILD-CLOUD.md",
        "GOVERNANCE.md",
        "ALM.md",
        "CHECKLIST.md",
        "PAC-DRY-RUN.md",
        "sources.json",
        "architecture.json",
    }
    src = json.loads((pack / "sources.json").read_text(encoding="utf-8"))["sources"]
    gov = (pack / "GOVERNANCE.md").read_text(encoding="utf-8")
    alm = (pack / "ALM.md").read_text(encoding="utf-8")
    pac = (pack / "PAC-DRY-RUN.md").read_text(encoding="utf-8")
    design_txt = (pack / "DESIGN.md").read_text(encoding="utf-8")
    gates = {
        "pack_files": required <= files,
        "entra_or_auth": "Entra" in arch.auth or "Authenticate" in arch.auth,
        "not_no_auth_model": not arch.auth.startswith("No authentication"),
        "europe": "Europe" in arch.environment_region or "EU" in gov,
        "learn_sources": all("learn.microsoft.com" in u or "microsoft.com" in u for u in src),
        "sources_nonempty": len(src) >= 3,
        "dlp_named": "Chat without Microsoft Entra ID authentication" in " ".join(arch.dlp_connectors),
        "pac_dry_run": "cs-agent pac plan" in alm or "pac solution" in pac,
        "no_secrets": not re.search(r"(client_secret|password\s*=)\s*\S+", design_txt + gov, re.IGNORECASE),
        "governance_metrics_hint": "Analytics" in (pack / "CHECKLIST.md").read_text(encoding="utf-8")
        or "App Insights" in (pack / "CHECKLIST.md").read_text(encoding="utf-8"),
    }
    return {
        "tier": arch.tier,
        "tier_label": arch.tier_label,
        "pattern": arch.pattern,
        "auth": arch.auth,
        "region": arch.environment_region,
        "systems": arch.intent.systems,
        "autonomous": arch.intent.autonomous,
        "multi_agent": arch.intent.multi_agent,
        "public_facing": arch.intent.public_facing,
        "gates": gates,
        "pass": all(gates.values()),
        "pack": str(pack.relative_to(ROOT)),
    }


def main() -> int:
    briefs = json.loads(BRIEFS.read_text(encoding="utf-8"))
    learn = _learn_urls()
    OUT.mkdir(parents=True, exist_ok=True)
    rows = []
    for b in briefs:
        intent = parse_brief(b["brief"])
        arch = design(intent)
        pack = write_pack(arch, OUT / b["id"])
        row = {"id": b["id"], "title": b["title"], **score_pack(arch, pack, learn)}
        rows.append(row)
    summary = {
        "n": len(rows),
        "passed": sum(1 for r in rows if r["pass"]),
        "failed": [r["id"] for r in rows if not r["pass"]],
        "tier_hist": {},
        "rows": rows,
    }
    for r in rows:
        summary["tier_hist"][str(r["tier"])] = summary["tier_hist"].get(str(r["tier"]), 0) + 1
    outp = ROOT / "docs" / "benchmark" / "results.json"
    outp.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(f"passed {summary['passed']}/{summary['n']} failed={summary['failed']} tiers={summary['tier_hist']}")
    print(f"wrote {outp}")
    return 0 if summary["passed"] == summary["n"] else 1


if __name__ == "__main__":
    raise SystemExit(main())

"""Slice 2 — golden briefs snapshot tests on key architecture sections."""

from __future__ import annotations

import json
from pathlib import Path

from cs_agent.architect import design
from cs_agent.intent import parse_brief
from cs_agent.pack import write_pack

GOLDENS = Path(__file__).resolve().parent / "goldens" / "briefs.json"


def _load() -> dict:
    return json.loads(GOLDENS.read_text(encoding="utf-8"))


def test_golden_briefs_key_sections(tmp_path: Path) -> None:
    data = _load()
    assert set(data) == {"hr_pto", "autonomous_email", "multi_agent_router", "public_faq"}

    for slug, case in data.items():
        intent = parse_brief(case["brief"])
        arch = design(intent)
        exp = case["expect"]

        if "audience" in exp:
            assert intent.audience == exp["audience"], slug
        if "region" in exp:
            assert intent.region == exp["region"], slug
        if "public_facing" in exp:
            assert intent.public_facing is exp["public_facing"], slug
        if "systems" in exp:
            for s in exp["systems"]:
                assert s in intent.systems, f"{slug} missing system {s}"
        assert arch.tier >= exp["min_tier"], f"{slug} tier {arch.tier}"
        if "pattern_contains" in exp:
            assert exp["pattern_contains"] in arch.pattern, slug
        if "auth_contains" in exp:
            assert exp["auth_contains"] in arch.auth, slug
        if "auth_forbids" in exp:
            assert exp["auth_forbids"] not in arch.auth, slug
        if "env_contains" in exp:
            assert exp["env_contains"] in arch.environment_region, slug
        if "knowledge_contains" in exp:
            assert any(exp["knowledge_contains"] in k for k in arch.knowledge), slug
        if "channels_contains" in exp:
            assert any(exp["channels_contains"] in c for c in arch.channels), slug
        if "tools_any" in exp:
            blob = " ".join(arch.tools)
            assert any(t in blob for t in exp["tools_any"]), slug

        pack = write_pack(arch, tmp_path / slug)
        design_txt = (pack / "DESIGN.md").read_text(encoding="utf-8")
        gov = (pack / "GOVERNANCE.md").read_text(encoding="utf-8")
        sources = (pack / "sources.json").read_text(encoding="utf-8")
        assert "Europe" in design_txt or "EU" in design_txt or "Europe" in gov, slug
        assert "learn.microsoft.com" in sources, slug
        assert (pack / "BUILD-CLOUD.md").is_file()
        assert (pack / "CHECKLIST.md").is_file()
        assert (pack / "ALM.md").is_file()

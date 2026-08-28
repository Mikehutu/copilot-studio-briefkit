"""CLI, PAC dry-run, KB source shape, FI language."""

from __future__ import annotations

import json
import re
from pathlib import Path

import pytest

from cs_agent import __version__
from cs_agent.architect import design
from cs_agent.cli import main
from cs_agent.intent import parse_brief
from cs_agent.pac import execute_pac, is_write_command, pac_status, plan_alm
from cs_agent.pack import write_pack

ROOT = Path(__file__).resolve().parents[1]
KB = ROOT / "kb"


def test_version():
    assert __version__ == "0.7.0"


def test_cli_ask(capsys):
    rc = main(["ask", "What", "is", "MCP"])
    assert rc == 0
    out = capsys.readouterr().out
    assert "learn.microsoft.com" in out


def test_cli_brief_json(capsys, tmp_path: Path):
    rc = main(["brief", "--json", "IT helpdesk ServiceNow Teams Finland"])
    assert rc == 0
    data = json.loads(capsys.readouterr().out)
    assert data["tier"] >= 2
    assert "Europe" in data["environment_region"]


def test_cli_brief_file(tmp_path: Path):
    p = tmp_path / "brief.txt"
    p.write_text("Finnish IT helpdesk Teams ServiceNow", encoding="utf-8")
    rc = main(["brief-file", str(p), "--out", str(tmp_path / "out")])
    assert rc == 0


def test_cli_pac_dry_run(capsys):
    rc = main(["pac", "plan"])
    assert rc == 0
    out = capsys.readouterr().out
    assert "SKIPPED (dry-run)" in out
    assert "pac solution import" in out


def test_cli_pac_execute_without_yes(capsys):
    rc = main(["pac", "plan", "--execute"])
    assert rc == 2
    assert "requires --i-confirm-yes" in capsys.readouterr().out


def test_cli_pac_status(capsys):
    rc = main(["pac", "status"])
    assert rc in (0, 1)  # 0 = EU confirmed, 1 = unconfirmed; never crash
    out = capsys.readouterr().out
    assert "PAC on PATH" in out


def test_pac_status_not_installed(monkeypatch):
    monkeypatch.setattr("cs_agent.pac.pac_on_path", lambda: False)
    st = pac_status()
    assert not st.installed
    assert not st.eu_ok
    assert "not found" in st.message.lower()


def test_cli_pac_status_not_installed_exit_0(monkeypatch, capsys):
    # Verifier finding: not-installed must be informational (exit 0), not a block.
    monkeypatch.setattr("cs_agent.pac.pac_on_path", lambda: False)
    rc = main(["pac", "status"])
    assert rc == 0
    assert "not found" in capsys.readouterr().out.lower()


def test_pac_status_scrubs_secrets(monkeypatch):
    monkeypatch.setattr("cs_agent.pac.pac_on_path", lambda: True)

    class FakeProc:
        stdout = "Profile\tregion\tcloud\ntoken=abc123 secret var password=hunter2"
        stderr = ""

    monkeypatch.setattr("cs_agent.pac.subprocess.run", lambda *a, **k: FakeProc())
    st = pac_status()
    blob = "\n".join(st.lines) + st.message
    assert "abc123" not in blob
    assert "hunter2" not in blob
    assert "REDACTED" in blob


def test_pac_status_eu_region_ok(monkeypatch):
    monkeypatch.setattr("cs_agent.pac.pac_on_path", lambda: True)
    monkeypatch.setattr(
        "cs_agent.pac._run_pac",
        lambda args: "Asia  crm4.dynamics.com  https://x.crm4.dynamics.com\n",
    )
    st = pac_status()
    assert st.eu_ok is True
    assert st.region == "Europe"


def test_pac_status_non_eu_blocks(monkeypatch):
    monkeypatch.setattr("cs_agent.pac.pac_on_path", lambda: True)
    monkeypatch.setattr(
        "cs_agent.pac._run_pac",
        lambda args: "united states  crm2.dynamics.com  https://x.crm2.dynamics.com\n",
    )
    st = pac_status()
    assert st.eu_ok is False
    assert "NOT the EU" in st.message or "Blocking" in st.message


def test_is_write_command_verbs():
    assert is_write_command("pac solution import --path x")
    assert is_write_command("pac solution publish")
    assert is_write_command("pac solution delete")
    assert is_write_command("pac auth create --environment https://x")
    assert not is_write_command("pac solution unpack --zipfile z")


def test_cli_pac_execute_refused(capsys):
    rc = main(["pac", "plan", "--execute", "--i-confirm-yes"])
    assert rc == 2
    assert "REFUSED" in capsys.readouterr().out


def test_execute_pac_never_runs_without_flags():
    cmd = "pac solution import --path ./x.zip"
    assert is_write_command(cmd)
    assert execute_pac(cmd, execute=False, confirmed_yes=False).startswith("SKIPPED")
    with pytest.raises(PermissionError):
        execute_pac(cmd, execute=True, confirmed_yes=True)


def test_plan_alm_has_europe_hint():
    plan = plan_alm()
    assert any("EU" in n or "crm4" in n for n in plan.notes + plan.commands)


def test_fi_swedish_languages():
    i = parse_brief("HR bot Teams Finland Swedish bilingual")
    assert "sv" in i.languages
    assert "fi" in i.languages


def test_gov_fi_notes(tmp_path: Path):
    a = design(parse_brief("HR PTO Workday Teams Finland Swedish"))
    pack = write_pack(a, tmp_path)
    gov = (pack / "GOVERNANCE.md").read_text(encoding="utf-8")
    assert "Finnish primary" in gov
    assert (pack / "PAC-DRY-RUN.md").is_file()
    assert "cs-agent pac plan" in (pack / "ALM.md").read_text(encoding="utf-8")


def test_kb_sources_are_https():
    text = (KB / "SOURCES.md").read_text(encoding="utf-8")
    urls = re.findall(r"https://[^\s|]+", text)
    assert len(urls) >= 10
    for u in urls:
        assert u.startswith("https://")
        assert " " not in u

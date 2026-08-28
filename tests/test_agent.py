"""Tests for CS enterprise agent."""

from pathlib import Path

from cs_agent.architect import design
from cs_agent.ask import ask
from cs_agent.intent import parse_brief
from cs_agent.pack import write_pack

ROOT = Path(__file__).resolve().parents[1]
KB = ROOT / "kb"


def test_parse_it_helpdesk_fi():
    brief = (
        "Finnish enterprise IT helpdesk agent for employees in Teams. "
        "Password reset guidance, ServiceNow tickets, SharePoint IT docs. EU only."
    )
    i = parse_brief(brief)
    assert i.audience == "internal"
    assert i.region == "eu-fi"
    assert "ServiceNow" in i.systems
    assert "Microsoft Teams" in i.channels


def test_teams_sharepoint_outlook_are_not_systems():
    """Channels (Teams) and knowledge sources (SharePoint) and mail triage
    (Outlook) must never surface as connector-action systems. Regression for
    the spurious 'Connector actions for Microsoft Teams / SharePoint' tools.
    """
    i = parse_brief(
        "Internal HR bot in Teams with SharePoint policies and Outlook email triage, PTO via Workday."
    )
    assert "Microsoft Teams" in i.channels
    assert "SharePoint" in i.knowledge_hints
    assert "Workday" in i.systems
    assert "Microsoft Teams" not in i.systems
    assert "SharePoint" not in i.systems
    assert "Outlook" not in i.systems

    a = design(i)
    tool_blob = " ".join(a.tools)
    assert "Connector actions for Microsoft Teams" not in tool_blob
    assert "Connector actions for SharePoint" not in tool_blob
    assert "Connector actions for Outlook" not in tool_blob
    assert "Connector actions for Workday" in tool_blob


def test_design_defaults_entra_and_eu():
    i = parse_brief("Internal HR bot for PTO with Workday and SharePoint policies")
    a = design(i)
    assert a.tier >= 2
    assert "Entra" in a.auth or "Microsoft" in a.auth
    assert "Europe" in a.environment_region
    assert "No authentication" not in a.auth


def test_no_auth_not_default_internal():
    a = design(parse_brief("Company FAQ bot for staff on Teams using SharePoint"))
    assert "No authentication" not in a.auth


def test_autonomous_tier():
    a = design(
        parse_brief(
            "Autonomous agent that triggers when email arrives and creates ServiceNow tickets"
        )
    )
    assert a.tier >= 4
    assert any("trigger" in t.lower() or "Event" in t for t in a.tools)


def test_write_pack(tmp_path: Path):
    a = design(parse_brief("IT helpdesk ServiceNow Teams Finland"))
    pack = write_pack(a, tmp_path)
    for name in (
        "DESIGN.md",
        "BUILD-CLOUD.md",
        "GOVERNANCE.md",
        "ALM.md",
        "DEPLOY.md",
        "CHECKLIST.md",
        "PAC-DRY-RUN.md",
        "sources.json",
        "architecture.json",
    ):
        assert (pack / name).is_file(), name
    deploy_txt = (pack / "DEPLOY.md").read_text(encoding="utf-8")
    assert "Human-executed, no silent import" in deploy_txt
    assert "crm4.dynamics.com" in deploy_txt
    design_txt = (pack / "DESIGN.md").read_text(encoding="utf-8")
    assert "Europe" in design_txt or "EU" in design_txt
    assert "learn.microsoft.com" in (pack / "sources.json").read_text(encoding="utf-8")


def test_ask_mcp():
    ans = ask("What is MCP in Copilot Studio?", KB)
    assert ans.files
    assert any("learn.microsoft.com" in s for s in ans.sources)


def test_ask_unknown_points_to_learn():
    ans = ask("xyzzy-nonexistent-foobar-12345", KB)
    assert "learn.microsoft.com" in ans.text.lower() or any(
        "learn.microsoft.com" in s for s in ans.sources
    )


def test_public_faq_not_sharepoint():
    i = parse_brief("Public website customer-facing FAQ agent using our public website knowledge")
    assert i.public_facing
    assert "SharePoint" not in i.knowledge_hints
    assert "Public website" in i.knowledge_hints


def test_approved_is_not_reporting():
    i = parse_brief("Internal knowledge agent using MCP tools against an approved server plus SharePoint")
    assert "reporting" not in i.actions


def test_mcp_brief_tier():
    a = design(parse_brief("Internal Teams agent using MCP tools plus SharePoint Finland"))
    assert a.tier >= 3
    assert any("MCP" in t for t in a.tools)


def test_kb_expanded_topics():
    for name in (
        "channels-publishing.md",
        "licensing.md",
        "generative-orchestration.md",
        "computer-use.md",
        "connectors-catalog.md",
        "observability-metrics.md",
        "ppac-governance.md",
    ):
        assert (KB / name).is_file(), name


def test_kb_observability_has_app_insights_dlp_name():
    text = (KB / "observability-metrics.md").read_text(encoding="utf-8")
    assert "Azure Application Insights" in text
    assert "Power CAT" in text
    assert "credit" in text.lower()


def test_kb_ppac_governance_docs_only():
    text = (KB / "ppac-governance.md").read_text(encoding="utf-8")
    assert "PPAC" in text or "Power Platform admin center" in text
    assert "Data policies" in text
    assert "never" in text.lower()  # no scripted policy PUT


def test_kb_publish_threat_model():
    text = (KB / "channels-publishing.md").read_text(encoding="utf-8")
    assert "threat model" in text.lower()
    assert "Direct Line" in text


def test_public_pack_has_threat_model(tmp_path: Path):
    a = design(parse_brief("Public website customer-facing FAQ agent using our public website knowledge"))
    pack = write_pack(a, tmp_path)
    design_txt = (pack / "DESIGN.md").read_text(encoding="utf-8")
    assert "Threat model" in design_txt
    assert "Direct Line" in design_txt


def test_internal_pack_threat_model_simple(tmp_path: Path):
    a = design(parse_brief("Internal HR bot PTO Workday Teams Finland"))
    pack = write_pack(a, tmp_path)
    design_txt = (pack / "DESIGN.md").read_text(encoding="utf-8")
    assert "Threat model" in design_txt
    assert "Internal-only agent" in design_txt
    # internal should not get external Direct Line warnings
    assert "Direct Line is a public endpoint" not in design_txt



def test_ask_dlp_connector_names():
    ans = ask("Chat without Microsoft Entra ID authentication DLP", KB)
    assert ans.files
    blob = ans.text + " ".join(ans.sources)
    assert "learn.microsoft.com" in blob


def test_ask_agent_flows():
    ans = ask("How are agent flows different from Power Automate cloud flows?", KB)
    assert ans.files
    blob = ans.text + " ".join(ans.sources)
    assert "learn.microsoft.com" in blob
    assert "agent-flows" in " ".join(ans.files) or "flow" in ans.text.lower()


def test_custom_connector_and_azure_escalation():
    a = design(
        parse_brief(
            "Internal Teams agent using a custom connector OpenAPI and high volume Azure Functions if throttled"
        )
    )
    assert a.tier >= 3
    assert any("Custom connector" in t for t in a.tools)
    assert any("Azure Functions" in r or "Logic Apps" in r for r in a.risks)


def test_ask_eudb():
    ans = ask("EU Data Boundary environments billing address", KB)
    assert "eu-finland" in " ".join(ans.files) or "EU" in ans.text

"""Map Intent → Architecture with EU/FI enterprise defaults."""

from __future__ import annotations

from .models import Architecture, Intent

LEARN = {
    "auth": "https://learn.microsoft.com/en-us/microsoft-copilot-studio/configuration-end-user-authentication",
    "dlp": "https://learn.microsoft.com/en-us/microsoft-copilot-studio/admin-data-loss-prevention",
    "knowledge": "https://learn.microsoft.com/en-us/microsoft-copilot-studio/knowledge-copilot-studio",
    "security": "https://learn.microsoft.com/en-us/microsoft-copilot-studio/security-and-governance",
    "mcp": "https://learn.microsoft.com/en-us/microsoft-copilot-studio/agent-extend-action-mcp",
    "autonomous": "https://learn.microsoft.com/en-us/microsoft-copilot-studio/guidance/autonomous-agents",
    "connected": "https://learn.microsoft.com/en-us/microsoft-copilot-studio/authoring-add-other-agents",
    "computer_use": "https://learn.microsoft.com/en-us/microsoft-copilot-studio/computer-use",
    "regions": "https://learn.microsoft.com/en-us/power-platform/admin/regions-overview",
    "teams": "https://learn.microsoft.com/en-us/microsoft-copilot-studio/publication-add-bot-to-microsoft-teams",
    "alm": "https://learn.microsoft.com/en-us/microsoft-copilot-studio/guidance/alm",
    "connectors": "https://learn.microsoft.com/en-us/connectors/connector-reference/",
    "ess": "https://learn.microsoft.com/en-us/microsoft-365/copilot/employee-self-service/overview",
    "flows": "https://learn.microsoft.com/en-us/microsoft-copilot-studio/flows-overview",
    "flows_faq": "https://learn.microsoft.com/en-us/microsoft-copilot-studio/flows-faqs",
    "integrations": "https://learn.microsoft.com/en-us/microsoft-copilot-studio/guidance/integrations",
    "custom_connectors": "https://learn.microsoft.com/en-us/connectors/custom-connectors/",
    "pa_limits": "https://learn.microsoft.com/en-us/power-automate/limits-and-config",
    "cs_quotas": "https://learn.microsoft.com/en-us/microsoft-copilot-studio/requirements-quotas",
    "logic_apps": "https://learn.microsoft.com/en-us/azure/logic-apps/logic-apps-overview",
}


def design(intent: Intent) -> Architecture:
    tier = 1
    pattern = "FAQ / knowledge agent"
    starter = None
    tools: list[str] = []
    knowledge = list(intent.knowledge_hints)
    generative = True
    risks: list[str] = []
    sources = [LEARN["knowledge"], LEARN["security"], LEARN["auth"], LEARN["regions"]]

    has_actions = bool(intent.actions or intent.systems)
    if has_actions:
        tier = 2
        pattern = "Structured self-service agent"
        starter = "Employee Self-Service (IT or HR) if applicable"
        sources.append(LEARN["ess"])
        sources.append(LEARN["connectors"])
        for s in intent.systems:
            tools.append(f"Connector actions for {s} (see connector reference)")
        if any("ticket" in a for a in intent.actions):
            tools.append("Create/update ticket via ITSM connector or agent flow")
        if any(a in intent.actions for a in ("password_reset_guidance",)):
            tools.append("Guided topic for password reset (no secret storage)")
        if any(a in intent.actions for a in ("pto_request", "time_off")):
            tools.append("HRIS connector: balance check + submit request")

    if intent.actions and any(
        a in intent.actions for a in ("approval_workflow", "invoice_handling", "email_triage", "reporting")
    ):
        tier = max(tier, 3)
        pattern = "Action / tool-using agent"
        tools.append("Agent flow for multi-step deterministic logic + approvals")
        sources.append(LEARN["flows"])
        sources.append(LEARN["flows_faq"])

    brief_l = intent.raw_brief.lower()
    if any(w in brief_l for w in ("power automate", "agent flow", "cloud flow")):
        tier = max(tier, 3)
        tools.append(
            "Agent flow tool: solution flow with When an agent calls the flow + Respond to the agent "
            "(convert PA cloud flow only one-way to CS capacity)"
        )
        sources.extend([LEARN["flows"], LEARN["flows_faq"]])

    if any(w in brief_l for w in ("custom connector", "openapi", "postman collection")):
        tier = max(tier, 3)
        tools.append(
            "Custom connector (OpenAPI/Postman REST wrapper; Tools → Custom connector → Power Apps portal)"
        )
        sources.append(LEARN["custom_connectors"])
        sources.append(LEARN["integrations"])

    if any(w in brief_l for w in ("high volume", "throttl", "rpm", "logic apps", "azure function")):
        risks.append(
            "If agent flow/PA hits limits: Dataverse custom API or plugin, Azure Functions; "
            "Logic Apps for Azure-native/VNet/SOAP — recreate connector from OpenAPI (not auto-shared from Logic Apps)"
        )
        sources.extend([LEARN["integrations"], LEARN["pa_limits"], LEARN["cs_quotas"], LEARN["logic_apps"]])

    if "mcp" in brief_l:
        tier = max(tier, 3)
        pattern = "Action / tool-using agent"
        tools.append("MCP server tools (generative orchestration required; classify MCP connector in DLP)")
        sources.append(LEARN["mcp"])

    if intent.autonomous:
        tier = max(tier, 4)
        pattern = "Autonomous event-driven agent"
        generative = True
        tools.append("Event trigger (email / Dataverse / schedule / file)")
        tools.append("Human-in-the-loop approval for high-risk actions")
        sources.append(LEARN["autonomous"])
        risks.append("Autonomous actions require sandbox, logging, kill switch, DLP on triggers")

    if intent.computer_use:
        tier = max(tier, 4)
        pattern = "Computer Use / legacy UI automation"
        tools.append("Computer Use / desktop flow (only if no API)")
        sources.append(LEARN["computer_use"])
        risks.append("CUA is last resort; prefer APIs/custom connectors")

    if intent.multi_agent:
        tier = max(tier, 5)
        pattern = "Multi-agent router with specialists"
        tools.append("Connected child agents with handoff rules")
        sources.append(LEARN["connected"])

    # Enterprise program always recommended as overlay for production
    if tier >= 2:
        sources.append(LEARN["alm"])
        sources.append(LEARN["dlp"])

    # Auth defaults
    if intent.audience == "internal" or not intent.public_facing:
        if "Microsoft Teams" in intent.channels and len(intent.channels) == 1:
            auth = "Authenticate with Microsoft (Entra via Teams/M365)"
        else:
            auth = "Authenticate manually with Microsoft Entra ID"
    else:
        auth = "Authenticate manually (Entra or OAuth2) — do NOT use No authentication for personal data"
        risks.append("External channel needs explicit threat model and WAF/CDN review for Direct Line")

    if intent.region.startswith("eu"):
        env_region = "Europe (EU/EFTA datacenters; align tenant + environments for EU Data Boundary)"
    else:
        env_region = "Match user base; document residency explicitly"
        risks.append("Non-EU region selected — confirm legal basis")

    dlp = [
        "Chat without Microsoft Entra ID authentication in Copilot Studio → Block for internal",
        "HTTP → Business or endpoint-filtered",
        "Microsoft Copilot Studio (triggers) → control if autonomous",
    ]
    if "SharePoint" in knowledge:
        dlp.append("Knowledge source with SharePoint and OneDrive in Copilot Studio → Business")
    if "Public website" in knowledge:
        dlp.append("Knowledge source with public websites and data in Copilot Studio → review")
    if any("MCP" in t or "mcp" in t.lower() for t in tools):
        dlp.append("MCP path uses connector DLP — classify MCP connector Business")
        sources.append(LEARN["mcp"])

    channels = list(intent.channels)
    if intent.audience == "internal" and "Microsoft Teams" not in channels:
        channels.insert(0, "Microsoft Teams")

    if not knowledge:
        knowledge = ["SharePoint (security-trimmed)"] if intent.audience != "external" else ["Public website"]

    tier_labels = {
        1: "Tier 1 Knowledge",
        2: "Tier 2 Self-service",
        3: "Tier 3 Action agents",
        4: "Tier 4 Autonomous/CUA",
        5: "Tier 5 Multi-agent",
        6: "Tier 6 Enterprise program",
    }

    # Production always implies program practices
    if tier >= 2:
        risks.append("Use Dev/Test/Prod EU environments and managed solutions for production")

    return Architecture(
        intent=intent,
        tier=tier,
        tier_label=tier_labels.get(tier, f"Tier {tier}"),
        pattern=pattern,
        auth=auth,
        environment_region=env_region,
        generative_orchestration=generative,
        knowledge=knowledge,
        tools=tools or ["None beyond generative answers"],
        channels=channels,
        dlp_connectors=dlp,
        risks=risks,
        sources=sorted(set(sources)),
        starter_template=starter,
    )

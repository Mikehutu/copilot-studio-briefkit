"""Parse free-text briefs into Intent."""

from __future__ import annotations

import re

from .models import Intent

_SYSTEM_KW = {
    "servicenow": "ServiceNow",
    "jira": "Jira",
    "workday": "Workday",
    "sap": "SAP",
    "salesforce": "Salesforce",
    "dynamics": "Dynamics 365",
    "dataverse": "Dataverse",
    "zendesk": "Zendesk",
    "hubspot": "HubSpot",
    "oracle": "Oracle",
}

_ACTION_KW = [
    ("password", "password_reset_guidance"),
    ("ticket", "create_or_check_ticket"),
    ("pto", "pto_request"),
    ("leave", "time_off"),
    ("invoice", "invoice_handling"),
    ("order", "order_status"),
    ("approv", "approval_workflow"),
    ("email", "email_triage"),
    ("schedule", "scheduling"),
    ("report", "reporting"),
]


def parse_brief(text: str) -> Intent:
    lower = text.lower()
    systems = [v for k, v in _SYSTEM_KW.items() if k in lower]
    actions = [a for k, a in _ACTION_KW if re.search(rf"\b{re.escape(k)}\w*", lower)]

    autonomous = any(w in lower for w in ("autonomous", "trigger", "without human", "event-driven"))
    multi_agent = any(w in lower for w in ("multi-agent", "router", "specialist agents", "child agent"))
    computer_use = any(w in lower for w in ("computer use", "cua", "legacy ui", "green screen", "rpa desktop"))
    public_facing = any(w in lower for w in ("public website", "customer-facing", "external customer", "anonymous"))

    audience = "external" if public_facing else "internal"
    if "partner" in lower or "b2b" in lower:
        audience = "mixed"

    channels: list[str] = []
    if "teams" in lower or audience == "internal":
        channels.append("Microsoft Teams")
    if "web" in lower or "website" in lower or public_facing:
        channels.append("Custom website / Direct Line")
    if "m365 copilot" in lower or "declarative" in lower:
        channels.append("Microsoft 365 Copilot")
    if not channels:
        channels.append("Microsoft Teams")

    knowledge_hints: list[str] = []
    if ("sharepoint" in lower or "policy" in lower or ("faq" in lower and not public_facing)):
        knowledge_hints.append("SharePoint")
    if "website" in lower or "public" in lower:
        knowledge_hints.append("Public website")
    if "pdf" in lower or "document" in lower or "manual" in lower:
        knowledge_hints.append("Documents")
    if not knowledge_hints and audience == "internal":
        knowledge_hints.append("SharePoint")

    # Name: first line or truncated
    first = text.strip().splitlines()[0].strip()
    name = re.sub(r"[^a-zA-Z0-9 _-]+", "", first)[:60] or "enterprise-agent"
    if len(name) < 4:
        name = "enterprise-agent"

    region = "eu-fi"
    if "us only" in lower or "united states" in lower:
        region = "us"

    languages = ["fi", "en"]
    if "swedish" in lower or "svenska" in lower or "ruotsi" in lower:
        languages.append("sv")

    missing: list[str] = []
    if not systems and any(a in actions for a in ("create_or_check_ticket", "pto_request")):
        missing.append("target_system_not_named")
    if audience == "external" and "auth" not in lower and "login" not in lower:
        missing.append("external_auth_model_unspecified")
    if autonomous and "approval" not in lower and "human" not in lower:
        missing.append("hitl_policy_unspecified_for_autonomous")

    return Intent(
        raw_brief=text.strip(),
        name=name,
        audience=audience,
        region=region,
        languages=sorted(set(languages)),
        systems=systems,
        actions=actions,
        knowledge_hints=knowledge_hints,
        channels=channels,
        autonomous=autonomous,
        multi_agent=multi_agent,
        computer_use=computer_use,
        public_facing=public_facing,
        missing=missing,
    )

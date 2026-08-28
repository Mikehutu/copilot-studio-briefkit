"""Domain models for CS enterprise agent."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass
class Intent:
    raw_brief: str
    name: str
    audience: str  # internal | external | mixed
    region: str  # eu-fi default
    languages: list[str] = field(default_factory=lambda: ["fi", "en"])
    systems: list[str] = field(default_factory=list)
    actions: list[str] = field(default_factory=list)
    knowledge_hints: list[str] = field(default_factory=list)
    channels: list[str] = field(default_factory=list)
    autonomous: bool = False
    multi_agent: bool = False
    computer_use: bool = False
    public_facing: bool = False
    missing: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class Architecture:
    intent: Intent
    tier: int
    tier_label: str
    pattern: str
    auth: str
    environment_region: str
    generative_orchestration: bool
    knowledge: list[str]
    tools: list[str]
    channels: list[str]
    dlp_connectors: list[str]
    risks: list[str]
    sources: list[str]
    starter_template: str | None = None

    def to_dict(self) -> dict[str, Any]:
        d = asdict(self)
        d["intent"] = self.intent.to_dict()
        return d

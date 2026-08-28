"""PAC assist: dry-run sketches only unless explicit execute flag.

Never prints secrets. Never runs write/import unless execute=True AND
the caller already received human YES (CLI requires --i-confirm-yes).

`pac status` is read-only: it inspects local auth profiles and orgs.
Even read-only subprocess output is scrubbed for tokens/secrets.
"""

from __future__ import annotations

import re
import shutil
import subprocess
from dataclasses import dataclass

WRITE_VERBS = ("import", "publish", "delete", "create --environment")

# Anything that looks like a credential/token/secret gets redacted before
# any output leaves this module. Conservative on purpose.
_SECRET_RE = re.compile(
    r"(?i)(token|secret|password|key|authorization|bearer|refresh_token|client_secret)"
    r"[=:\s]\S+"
)

_EU_HINTS = ("europe", "eu", "crm4", "crm14", "crm15", "crm16", "deu", "fra", "gbr")


@dataclass(frozen=True)
class PacPlan:
    installed: bool
    commands: list[str]
    notes: list[str]


@dataclass(frozen=True)
class PacStatus:
    installed: bool
    message: str
    region: str | None
    eu_ok: bool
    lines: list[str]


def pac_on_path() -> bool:
    return shutil.which("pac") is not None


def plan_alm(dev_url: str = "https://<dev>.crm4.dynamics.com", solution: str = "<Solution>") -> PacPlan:
    cmds = [
        f'pac auth create --environment "{dev_url}"',
        f'pac solution export --name "{solution}" --path ./exports/sol.zip --managed false',
        "pac solution unpack --zipfile ./exports/sol.zip --folder ./src/solution",
        f'pac solution export --name "{solution}" --path ./exports/sol_managed.zip --managed true',
        'pac auth create --environment "https://<test>.crm4.dynamics.com"',
        "pac solution import --path ./exports/sol_managed.zip --force-overwrite",
    ]
    notes = [
        "Dry-run only: copy-paste after you authenticate to YOUR tenant.",
        "EU: prefer *.crm4.dynamics.com (Europe) environments.",
        "Do not run import without printed pre-flight + human YES.",
        "Never put secrets in CLI args; use PAC profiles / env vars.",
    ]
    return PacPlan(installed=pac_on_path(), commands=cmds, notes=notes)


def _scrub(text: str) -> str:
    """Redact anything that looks like a secret and strip ANSI control codes."""
    text = _SECRET_RE.sub(r"\1=***REDACTED***", text)
    # strip ANSI escape sequences that some CLI versions emit on color TTYs
    ansi = re.compile(r"\x1b\[[0-9;]*[A-Za-z]")
    return ansi.sub("", text)


def _run_pac(args: list[str]) -> str:
    """Run read-only `pac` subcommand; return scrubbed stdout+stderr."""
    proc = subprocess.run(
        ["pac", *args],
        capture_output=True,
        text=True,
        timeout=30,
        check=False,
    )
    return _scrub((proc.stdout or "") + "\n" + (proc.stderr or ""))


def _region_from(text: str) -> str | None:
    """Best-effort region/org classifier from `pac org list`/`auth list` output."""
    low = text.lower()
    for hint in ("europe", "eu"):
        if hint in low:
            return "Europe"
    m = re.search(r"crm(\d+)\.dynamics\.com", low)
    if m:
        num = int(m.group(1))
        # classic Europe instances are crm4/crm14/crm15/crm16
        if num in (4, 14, 15, 16):
            return "Europe"
        return f"Non-Europe (crm{num})"
    if "united states" in low or "u.s." in low or "north america" in low:
        return "Non-Europe (US)"
    if any(h in low for h in ("asia", "japan", "india", "australia", "canada", "south america")):
        return "Non-Europe"
    return None


def pac_status() -> PacStatus:
    """Read-only tenant status. Never writes. Never leaks secrets.

    Verify each environment lives in the EU region before proceeding with
    any import work.
    """
    if not pac_on_path():
        return PacStatus(
            installed=False,
            message=(
                "PAC CLI not found on PATH. Install: https://learn.microsoft.com/en-us/power-platform/developer/cli/introduction"
            ),
            region=None,
            eu_ok=False,
            lines=[],
        )

    try:
        auth_text = _run_pac(["auth", "list"])
    except (OSError, subprocess.TimeoutExpired):
        return PacStatus(
            installed=True,
            message="PAC is installed but `pac auth list` failed (not logged in to any tenant?).",
            region=None,
            eu_ok=False,
            lines=[],
        )

    org_text = ""
    try:
        org_text = _run_pac(["org", "list"])
    except (OSError, subprocess.TimeoutExpired):
        org_text = ""

    combined = auth_text + "\n" + org_text
    region = _region_from(combined)
    eu_ok = region == "Europe"
    lines = [ln for ln in combined.splitlines() if ln.strip()]

    if not eu_ok:
        msg = (
            "PAC auth/org could not be confirmed as Europe (EU/EFTA). "
            "Do NOT proceed with import work against this tenant."
        ) if region is None else (
            f"PAC tenant region is {region} — NOT the EU/EFTA baseline. "
            "Blocking work against this tenant."
        )
    else:
        msg = "PAC tenant confirmed Europe (EU/EFTA). Read-only status passed."

    return PacStatus(installed=True, message=msg, region=region, eu_ok=eu_ok, lines=lines)


def is_write_command(cmd: str) -> bool:
    low = cmd.lower()
    return any(v in low for v in WRITE_VERBS)


def execute_pac(cmd: str, *, execute: bool, confirmed_yes: bool) -> str:
    """Refuse writes unless both flags. Tests must keep execute=False."""
    if not execute or not confirmed_yes:
        return f"SKIPPED (dry-run): {cmd}"
    if is_write_command(cmd):
        raise PermissionError("Refusing PAC write without live-tenant consent path")
    raise PermissionError("Live PAC execution is not enabled in this build")

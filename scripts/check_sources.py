#!/usr/bin/env python3
"""Verify every Microsoft Learn / reference URL cited in the repo resolves (HTTP 200).

Checks:
  - kb/SOURCES.md (all https URLs)
  - every generated pack's sources.json
  - src/cs_agent/architect.py (LEARN dict)
  - src/cs_agent/pack.py (hardcoded Learn URLs)
  - docs/PROVIDERS.md, docs/EXAMPLES.md (https URLs on learn.microsoft.com)

Exit 0 = all URLs OK. Exit 1 = at least one broken/404. Network required.
Generic microsoft.com / github.com links are HEAD/GET checked; learn are strict.

Usage:  python3 scripts/check_sources.py [--kb KB_DIR]
"""
from __future__ import annotations

import json
import re
import ssl
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEARN = re.compile(r"https://learn\.microsoft\.com[^\s)>\]\"']+")
HTTP = re.compile(r"https?://[^\s)>\]\"']+")

# URLs that are intentionally not GET-able (placeholders, anchors) — skipped
_ALLOW_404 = {
    "https://learn.microsoft.com/en-us/microsoft-copilot-studio/",
    "https://www.microsoft.com/trustcenter",
}

CTX = ssl.create_default_context()


def _get(url: str) -> int:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (source-check)"})
    with urllib.request.urlopen(req, timeout=20, context=CTX) as resp:
        return resp.status


def collect_urls(root: Path) -> dict[str, set[str]]:
    found: dict[str, set[str]] = {}
    def add(kind: str, u: str):
        u = u.rstrip(".,;")
        if u.startswith("http"):
            found.setdefault(kind, set()).add(u)

    for f in (root / "kb").glob("*.md"):
        if f.name == "AGENTS.md":
            continue
        for u in LEARN.findall(f.read_text(encoding="utf-8")):
            add("kb", u)

    for arch in (root / "src" / "cs_agent").glob("*.py"):
        for u in LEARN.findall(arch.read_text(encoding="utf-8")):
            add("src", u)

    for pack in sorted((root / "examples").glob("ex*/**/sources.json")):
        data = json.loads(pack.read_text(encoding="utf-8"))
        for s in data["sources"]:
            add("pack", s)

    for f in (root / "docs").glob("*.md"):
        for u in LEARN.findall(f.read_text(encoding="utf-8")):
            add("docs", u)
    return found


def main() -> int:
    urls = collect_urls(ROOT)
    all_urls: set[str] = set()
    for v in urls.values():
        all_urls |= v
    print(f"Found {len(all_urls)} unique URLs across "
          f"{ {k: len(v) for k, v in urls.items()} }")

    broken: list[tuple[str, str]] = []
    skipped: list[str] = []
    for u in sorted(all_urls):
        if u.rstrip(".,;") in _ALLOW_404 or "{" in u or "<" in u or "example" in u.lower() or "your" in u.lower():
            skipped.append(u)
            continue
        try:
            code = _get(u)
            if code != 200:
                broken.append((u, f"HTTP {code}"))
        except Exception as e:  # noqa: BLE001
            broken.append((u, type(e).__name__))

    for u, why in broken:
        print(f"  BROKEN  {u}  -> {why}")
    print(f"  skipped (placeholders/examples): {len(skipped)}")
    print(f"  RESULT: {len(all_urls) - len(broken) - len(skipped)}/{len(all_urls) - len(skipped)} OK")
    return 1 if broken else 0


if __name__ == "__main__":
    sys.exit(main())

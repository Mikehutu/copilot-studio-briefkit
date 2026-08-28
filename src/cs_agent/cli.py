"""CLI: cs-agent ask | brief"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .architect import design
from .ask import ask as kb_ask
from .intent import parse_brief
from .pac import execute_pac, plan_alm
from .pack import write_pack

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_KB = ROOT / "kb"
DEFAULT_OUT = ROOT / "out"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="cs-agent",
        description="Copilot Studio Enterprise Agent — Q&A and brief→solution packs (EU/FI defaults)",
    )
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_ask = sub.add_parser("ask", help="Answer from local official KB")
    p_ask.add_argument("question", nargs="+")
    p_ask.add_argument("--kb", type=Path, default=DEFAULT_KB)

    p_brief = sub.add_parser("brief", help="R-PIV design pack from a business brief")
    p_brief.add_argument("text", nargs="+", help="Brief text")
    p_brief.add_argument("--out", type=Path, default=DEFAULT_OUT)
    p_brief.add_argument("--json", action="store_true", help="Print architecture JSON only")

    p_file = sub.add_parser("brief-file", help="Brief from a text file")
    p_file.add_argument("path", type=Path)
    p_file.add_argument("--out", type=Path, default=DEFAULT_OUT)

    p_pac = sub.add_parser("pac", help="PAC ALM sketches (dry-run by default)")
    p_pac.add_argument("action", choices=["plan", "status"], nargs="?", default="plan")
    p_pac.add_argument("--execute", action="store_true", help="Attempt live PAC (blocked unless --i-confirm-yes)")
    p_pac.add_argument("--i-confirm-yes", action="store_true", dest="confirm_yes")

    args = parser.parse_args(argv)

    if args.cmd == "ask":
        q = " ".join(args.question)
        ans = kb_ask(q, args.kb)
        print(ans.text)
        print("\n## Sources")
        for s in ans.sources:
            print(f"- {s}")
        return 0

    if args.cmd in ("brief", "brief-file"):
        if args.cmd == "brief-file":
            text = args.path.read_text(encoding="utf-8")
            out = args.out
        else:
            text = " ".join(args.text)
            out = args.out
        intent = parse_brief(text)
        arch = design(intent)
        if getattr(args, "json", False):
            print(json.dumps(arch.to_dict(), indent=2))
            return 0
        pack = write_pack(arch, out)
        print(f"Solution pack written: {pack}")
        print(f"Tier: {arch.tier_label} | Auth: {arch.auth}")
        print(f"Open: {pack / 'DESIGN.md'}")
        if intent.missing:
            print("Missing fields to resolve:", ", ".join(intent.missing))
        return 0

    if args.cmd == "pac":
        if args.action == "status":
            from .pac import pac_status

            st = pac_status()
            print(f"PAC on PATH: {st.installed}")
            print(st.message)
            if st.region:
                print(f"Region (inferred): {st.region}")
            for ln in st.lines[:40]:
                print(f"  {ln}")
            # not-installed = informational (0); non-EU/unconfirmed = block (1)
            if not st.installed:
                return 0
            return 1 if not st.eu_ok else 0

        if args.execute and not args.confirm_yes:
            print("REFUSED: --execute requires --i-confirm-yes")
            return 2
        plan = plan_alm()
        print(f"PAC on PATH: {plan.installed}")
        print("Action:", args.action)
        for n in plan.notes:
            print(f"- {n}")
        print("\n## Commands")
        for c in plan.commands:
            try:
                print(execute_pac(c, execute=args.execute, confirmed_yes=args.confirm_yes))
            except PermissionError as exc:
                print(f"REFUSED: {exc}")
                return 2
        return 0

    return 1


if __name__ == "__main__":
    sys.exit(main())

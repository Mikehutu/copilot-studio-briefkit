"""Simple KB Q&A over local markdown (keyword retrieval)."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Answer:
    text: str
    sources: list[str]
    files: list[str]


def load_kb(kb_dir: Path) -> list[tuple[str, str]]:
    docs: list[tuple[str, str]] = []
    for p in sorted(Path(kb_dir).glob("*.md")):
        docs.append((p.name, p.read_text(encoding="utf-8")))
    return docs


def ask(question: str, kb_dir: Path) -> Answer:
    docs = load_kb(kb_dir)
    q_tokens = {t for t in re.findall(r"[a-z0-9]{3,}", question.lower())}
    scored: list[tuple[int, str, str]] = []
    for name, body in docs:
        b_low = body.lower()
        score = sum(1 for t in q_tokens if t in b_low)
        # boost filename hits
        score += sum(2 for t in q_tokens if t in name.lower())
        if score:
            scored.append((score, name, body))
    scored.sort(key=lambda x: x[0], reverse=True)
    if not scored:
        return Answer(
            text=(
                "No local KB match. Search official docs: "
                "https://learn.microsoft.com/en-us/microsoft-copilot-studio/ "
                "Do not invent product behavior."
            ),
            sources=["https://learn.microsoft.com/en-us/microsoft-copilot-studio/"],
            files=[],
        )

    top = scored[:3]
    chunks: list[str] = []
    files: list[str] = []
    urls: list[str] = []
    for _, name, body in top:
        files.append(name)
        # extract urls
        urls.extend(re.findall(r"https://[^\s)>\"]+", body))
        # first substantive paragraphs
        paras = [p.strip() for p in body.split("\n\n") if p.strip() and not p.strip().startswith("#")]
        chunks.append(f"### From `{name}`\n" + "\n\n".join(paras[:3]))

    # dedupe urls preserve order
    seen: set[str] = set()
    sources: list[str] = []
    for u in urls:
        u = u.rstrip(".,;")
        if u not in seen and "microsoft" in u:
            seen.add(u)
            sources.append(u)
    if not sources:
        sources = ["https://learn.microsoft.com/en-us/microsoft-copilot-studio/"]

    text = (
        f"**Q:** {question}\n\n"
        + "\n\n".join(chunks)
        + "\n\n---\nGrounding rule: if this conflicts with Learn, Learn wins."
    )
    return Answer(text=text, sources=sources[:12], files=files)

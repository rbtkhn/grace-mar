"""Shared helpers for session checkpoints and handoff packets (runtime work layer only)."""

from __future__ import annotations

import re
from pathlib import Path

# Headings emitted by scripts/runtime/memory_brief.py
MB_BEST = "## Best Matches"
MB_TAKEAWAYS = "## Expanded Takeaways"


def slug(text: str, max_len: int = 48) -> str:
    s = text.lower().strip()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    s = s.strip("-")
    if not s:
        s = "checkpoint"
    return s[:max_len].rstrip("-")


def seeds_from_memory_brief(path: Path) -> tuple[str, list[str]]:
    """Return (objective_hint, established_bullets) from a memory brief Markdown file."""
    if not path.is_file():
        return "", []
    raw = path.read_text(encoding="utf-8")
    lane = ""
    query = ""
    for line in raw.splitlines():
        if line.startswith("Lane:"):
            lane = line.split("Lane:", 1)[1].strip()
        if line.startswith("Query:"):
            query = line.split("Query:", 1)[1].strip()
    if lane or query:
        objective = "Continue runtime lane work"
        if lane:
            objective += f" ({lane})"
        if query:
            objective += f" — query: {query}"
        objective += ". See Best Matches / Expanded Takeaways below for seeds."
    else:
        objective = "Continue work from linked memory brief (runtime-only)."

    established: list[str] = []
    for section_title, dest in ((MB_BEST, established), (MB_TAKEAWAYS, established)):
        block = _section_under_heading(raw, section_title)
        if not block:
            continue
        for bl in block.splitlines():
            bl = bl.strip()
            if bl.startswith("- "):
                dest.append(bl[2:].strip())
            elif bl.startswith("* "):
                dest.append(bl[2:].strip())

    if not established:
        established = ["_(No structured seed from memory brief; edit \"What seems established\".)_"]

    return objective, established


def _section_under_heading(text: str, heading: str) -> str:
    lines = text.splitlines()
    start = None
    for i, line in enumerate(lines):
        if line.strip() == heading.strip():
            start = i + 1
            break
    if start is None:
        return ""
    out: list[str] = []
    for line in lines[start:]:
        if line.startswith("## ") and line.strip() != heading.strip():
            break
        out.append(line)
    return "\n".join(out).strip()


def parse_built_line(body: str) -> str | None:
    for line in body.splitlines():
        line = line.strip()
        if line.startswith("Built:"):
            return line.split("Built:", 1)[1].strip()
    return None


def parse_field(body: str, prefix: str) -> str | None:
    for line in body.splitlines():
        line = line.strip()
        if line.startswith(prefix):
            return line[len(prefix) :].strip()
    return None


def extract_section(body: str, heading: str) -> str:
    """Return lines under ## heading until next ## or EOF."""
    return _section_under_heading(body, f"## {heading}")


def section_bullets(section_md: str) -> list[str]:
    out: list[str] = []
    for line in section_md.splitlines():
        line = line.strip()
        if line.startswith(("- ", "* ")):
            out.append(line[2:].strip())
    return out

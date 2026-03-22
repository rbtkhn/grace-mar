"""Prompt.py updates: append bullets (legacy) or rebuild YOUR * sections from self.md IX."""

from __future__ import annotations

import re

PROMPT_SECTION_HEADERS = {
    "YOUR KNOWLEDGE": "## YOUR KNOWLEDGE (from observations)",
    "YOUR CURIOSITY": "## YOUR CURIOSITY (what catches your attention)",
    "YOUR PERSONALITY": "## YOUR PERSONALITY (observed)",
}

# Rebuild: section start → next section start (exclusive end)
_REBUILD_SPANS = (
    (
        "## YOUR KNOWLEDGE (from observations)",
        "## YOUR CURIOSITY (what catches your attention)",
        "knowledge",
    ),
    (
        "## YOUR CURIOSITY (what catches your attention)",
        "## YOUR PERSONALITY (observed)",
        "curiosity",
    ),
    (
        "## YOUR PERSONALITY (observed)",
        "## IMPORTANT CONSTRAINTS",
        "personality",
    ),
)

_IX_A_FACTS = re.compile(
    r"#### Facts \(LEARN-nnn\)\s*\n\n```yaml\n(.*?)\n```",
    re.DOTALL,
)
_IX_B = re.compile(
    r"### IX-B\. CURIOSITY.*?```yaml\n(.*?)\n```",
    re.DOTALL,
)
_IX_C = re.compile(
    r"### IX-C\..*?```yaml\n(.*?)\n```",
    re.DOTALL,
)


def insert_prompt_addition(prompt_content: str, prompt_section: str, addition: str) -> str:
    """
    Insert one bullet under an explicit section header (legacy append-style
    prompt merge used by the pipeline).
    """
    line = f"- {addition.strip()}"
    if not addition.strip() or line in prompt_content:
        return prompt_content

    section_key = (prompt_section or "").strip().upper()
    header = PROMPT_SECTION_HEADERS.get(section_key)
    if header and header in prompt_content:
        start = prompt_content.find(header)
        next_header = prompt_content.find("\n## ", start + len(header))
        if next_header == -1:
            next_header = len(prompt_content)
        section_block = prompt_content[start:next_header]
        if line in section_block:
            return prompt_content
        insertion = f"{header}\n\n{line}\n"
        return prompt_content.replace(header + "\n", insertion, 1)

    if section_key == "YOUR KNOWLEDGE":
        return prompt_content.replace("## WHAT YOU LOVE", line + "\n\n## WHAT YOU LOVE", 1)
    if section_key in ("YOUR CURIOSITY", "YOUR PERSONALITY"):
        return prompt_content.replace("## HOW YOU HANDLE THINGS", line + "\n\n## HOW YOU HANDLE THINGS", 1)
    return prompt_content


def _topics_from_topic_lines(yaml_body: str) -> list[str]:
    out: list[str] = []
    for line in yaml_body.splitlines():
        m = re.match(r"^\s*topic:\s*(.+)$", line)
        if m:
            t = m.group(1).strip().strip("\"'")
            if t:
                out.append(t)
    return out


def _observations_from_ix_c(yaml_body: str) -> list[str]:
    out: list[str] = []
    for line in yaml_body.splitlines():
        m = re.match(r"^\s*observation:\s*(.+)$", line)
        if m:
            t = m.group(1).strip().strip("\"'")
            if t:
                out.append(t)
    return out


def _fmt_bullets(items: list[str], empty_msg: str) -> str:
    if not items:
        return f"- {empty_msg}\n"
    return "\n".join(f"- {b}" for b in items) + "\n"


def rebuild_observation_sections_from_self(prompt_content: str, self_content: str) -> str:
    """
    Replace YOUR KNOWLEDGE / CURIOSITY / PERSONALITY in SYSTEM_PROMPT with bullets from
    IX-A Facts ``topic:``, IX-B ``topic:``, IX-C ``observation:`` lines.

    Opt-in via candidate ``prompt_merge_mode: rebuild_ix``. Narrative bullets in those
    sections are replaced.
    """
    m_a = _IX_A_FACTS.search(self_content)
    m_b = _IX_B.search(self_content)
    m_c = _IX_C.search(self_content)
    yaml_a = m_a.group(1) if m_a else ""
    yaml_b = m_b.group(1) if m_b else ""
    yaml_c = m_c.group(1) if m_c else ""

    bodies = {
        "knowledge": _fmt_bullets(
            _topics_from_topic_lines(yaml_a),
            "(no IX-A Facts topic lines yet — merge from pipeline)",
        ),
        "curiosity": _fmt_bullets(
            _topics_from_topic_lines(yaml_b),
            "(no IX-B topic lines yet)",
        ),
        "personality": _fmt_bullets(
            _observations_from_ix_c(yaml_c),
            "(no IX-C observation lines yet)",
        ),
    }

    note = (
        "(Regenerated from self.md IX list entries — pipeline `rebuild_ix`. "
        "Narrative bullets are not preserved in this mode.)\n\n"
    )

    out = prompt_content
    for h_start, h_end, key in _REBUILD_SPANS:
        start = out.find(h_start)
        if start == -1:
            continue
        end = out.find(h_end, start + len(h_start))
        if end == -1:
            continue
        block = h_start + "\n\n" + note + bodies[key] + "\n"
        out = out[:start] + block + out[end:]

    return out

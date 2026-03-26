"""Structured insertion into canonical EVIDENCE (self-archive.md; ACTIVITY LOG, READING LIST)."""

from __future__ import annotations

import re

_ATTESTATION = re.compile(r"\n## VI\. ATTESTATION LOG")

# First pipeline READ merge: replace empty list
_READING_ENTRIES_EMPTY = re.compile(
    r"(## I\. READING LIST.*?```yaml\n)(entries:\s*\[\]\s*\n)",
    re.DOTALL,
)
# Later merges: insert before the example comment inside the same fenced block
_READING_BEFORE_EXAMPLE = re.compile(
    r"(## I\. READING LIST.*?```yaml\n)(.*?)(\n# Example entry format:)",
    re.DOTALL,
)


def append_act_entry(evidence_content: str, act_entry_fragment: str) -> str:
    """
    Insert a new ``- id: ACT-...`` block before ``## VI. ATTESTATION LOG``,
    or append at end if the heading is missing.
    """
    m = _ATTESTATION.search(evidence_content)
    if m:
        return evidence_content[: m.start()] + act_entry_fragment + evidence_content[m.start() :]
    return evidence_content + act_entry_fragment


def _format_read_item(read_id: str, title: str, evidence_tier: int, status: str) -> str:
    safe_title = title[:500].replace('"', "'")
    return f"""  - id: {read_id}
    title: "{safe_title}"
    type: book
    status: {status}
    evidence_tier: {evidence_tier}
    source: pipeline merge
"""


def upsert_reading_list_entry(
    evidence_content: str,
    *,
    read_id: str,
    title: str,
    evidence_tier: int = 3,
    status: str = "completed",
) -> str:
    """
    Insert into § I. READING LIST: replace ``entries: []`` on first use; otherwise
    append a list item before ``# Example entry format:``.
    If neither pattern matches, returns content unchanged.
    """
    block = _format_read_item(read_id, title, evidence_tier, status)

    m_empty = _READING_ENTRIES_EMPTY.search(evidence_content)
    if m_empty:
        replacement = m_empty.group(1) + "entries:\n" + block + "\n"
        return evidence_content[: m_empty.start()] + replacement + evidence_content[m_empty.end() :]

    m_ex = _READING_BEFORE_EXAMPLE.search(evidence_content)
    if m_ex:
        insert = "\n" + block
        return evidence_content[: m_ex.start(3)] + insert + evidence_content[m_ex.start(3) :]

    return evidence_content


# Back-compat alias
def insert_reading_list_entry(
    evidence_content: str,
    *,
    read_id: str,
    title: str,
    evidence_tier: int = 3,
    status: str = "completed",
) -> str:
    return upsert_reading_list_entry(
        evidence_content,
        read_id=read_id,
        title=title,
        evidence_tier=evidence_tier,
        status=status,
    )

"""Insert IX-A / IX-B / IX-C YAML list items into self.md fenced blocks."""

from __future__ import annotations

import re

# IX-A: LEARN entries live under #### Facts (LEARN-nnn), not the earlier books_read block.
IX_A_FACTS_ENTRIES = re.compile(
    r"(#### Facts \(LEARN-nnn\)\s*\n\n```yaml\nentries:\s*\n)(.*?)(\n```)",
    re.DOTALL,
)
IX_B_BLOCK = re.compile(
    r"(### IX-B\. CURIOSITY.*?```yaml\nentries:\s*\n)(.*?)(\n```)",
    re.DOTALL,
)
IX_C_BLOCK = re.compile(
    r"(### IX-C\..*?```yaml\nentries:\s*\n)(.*?)(\n```)",
    re.DOTALL,
)


def insert_ix_a_entry(self_content: str, new_entry: str) -> str:
    """Append one LEARN list item in the Facts (LEARN-nnn) ``entries:`` block."""
    m = IX_A_FACTS_ENTRIES.search(self_content)
    if not m:
        return self_content
    return self_content[: m.end(2)] + new_entry + self_content[m.start(3) :]


def insert_ix_b_entry(self_content: str, new_entry: str) -> str:
    """Append one CUR list item before the closing ``` of the IX-B yaml block."""
    m = IX_B_BLOCK.search(self_content)
    if not m:
        return self_content
    return self_content[: m.end(2)] + new_entry + self_content[m.start(3) :]


def insert_ix_c_entry(self_content: str, new_entry: str) -> str:
    """Append one PER list item before the closing ``` of the IX-C yaml block."""
    m = IX_C_BLOCK.search(self_content)
    if not m:
        return self_content
    return self_content[: m.end(2)] + new_entry + self_content[m.start(3) :]

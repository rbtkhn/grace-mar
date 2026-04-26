"""Insert IX-A / IX-B / IX-C YAML list items into self.md fenced blocks."""

from __future__ import annotations

import re

# IX-A: LEARN entries live under #### Facts (LEARN-nnn), not the earlier books_read block.
# Close the list at the *Facts* block only: the fence immediately before `## IX-B`, so
# a later `` ```yaml ``/`` entries:`` block under IX-B is never conflated with IX-A.
IX_A_FACTS_ENTRIES = re.compile(
    r"(#### Facts \(LEARN-nnn\)\s*\n\n```yaml\n)(entries:\s*\n)([\s\S]*?)(?=```\s*\n+(?:---\s*\n+)*#+\s*IX-B\.\s*CURIOSITY)",
    re.DOTALL,
)
# `##` / `###` profiles; end IX-B list at the fence before IX-C.
IX_B_BLOCK = re.compile(
    r"(#+\s*IX-B\.\s*CURIOSITY.*?\n```yaml\n)(entries:\s*\n)([\s\S]*?)(?=```\s*\n+(?:---\s*\n+)*#+\s*IX-C\.)",
    re.DOTALL,
)
# Close IX-C at the fence before `---` + "END OF FILE" (reseeded profile) or end-of-string.
IX_C_BLOCK = re.compile(
    r"(#+\s*IX-C\..*?\n```yaml\n)(entries:\s*\n)([\s\S]*?)(?=```\s*(?:\n+---\s*\n+END OF FILE|\s*$))",
    re.DOTALL,
)


def insert_ix_a_entry(self_content: str, new_entry: str) -> str:
    """Append one LEARN list item in the Facts (LEARN-nnn) ``entries:`` block."""
    m = IX_A_FACTS_ENTRIES.search(self_content)
    if not m:
        return self_content
    return self_content[: m.end(3)] + new_entry + self_content[m.end(3) :]


def insert_ix_b_entry(self_content: str, new_entry: str) -> str:
    """Append one CUR list item before the closing ``` of the IX-B yaml block."""
    m = IX_B_BLOCK.search(self_content)
    if not m:
        return self_content
    return self_content[: m.end(3)] + new_entry + self_content[m.end(3) :]


def insert_ix_c_entry(self_content: str, new_entry: str) -> str:
    """Append one PER list item before the closing ``` of the IX-C yaml block."""
    m = IX_C_BLOCK.search(self_content)
    if not m:
        return self_content
    return self_content[: m.end(3)] + new_entry + self_content[m.end(3) :]

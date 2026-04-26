"""
Shared parsing for recursion-gate.md candidate blocks.

One regex shape and section slicing for dashboards, review, and metrics — avoids drift
between recursion_gate_review and work_dev/build_dashboard.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Iterator

# ### CANDIDATE-123 optional (title)
# ```yaml
# ...
# ```
CANDIDATE_BLOCK_RE = re.compile(
    r"^### (CANDIDATE-\d+)(?:\s*\(([^)]*)\))?\s*\n```yaml\n(.*?)```",
    re.MULTILINE | re.DOTALL,
)


def split_gate_sections(full_md: str) -> tuple[str, str]:
    """
    Split at the actual `## Processed` heading.
    Returns (active_section_before_processed, processed_section_without_heading).
    """
    marker = re.search(r"^## Processed\s*$", full_md, re.MULTILINE)
    if not marker:
        return full_md, ""
    return full_md[: marker.start()], full_md[marker.end() :]


def pending_candidates_region(full_md: str) -> str:
    """Slice between `## Candidates` and the real `## Processed` section heading.

    Important: prose may mention ``## Processed`` in backticks (or inline) *before* the
    actual section; use the same `^## Processed\\s*$` anchor as `split_gate_sections`.
    """
    active, _proc = split_gate_sections(full_md)
    m = re.search(r"^## Candidates\s*$", active, re.MULTILINE)
    if not m:
        return ""
    return active[m.start() :]


def iter_candidate_yaml_blocks(text: str) -> Iterator[tuple[str, str, str]]:
    """Yield (candidate_id, title, yaml_body) for each fenced candidate block in text."""
    for m in CANDIDATE_BLOCK_RE.finditer(text):
        yield m.group(1), (m.group(2) or "").strip(), m.group(3)


def iter_pending_yaml_blobs(full_md: str) -> list[str]:
    """YAML bodies with status: pending inside the pending candidates region only."""
    region = pending_candidates_region(full_md)
    out: list[str] = []
    for _cid, _title, yaml_body in iter_candidate_yaml_blocks(region):
        if re.search(r"^status:\s*pending\s*$", yaml_body, re.MULTILINE):
            out.append(yaml_body)
    return out


def yaml_blob_provenance_fraction(yaml_body: str) -> float:
    """0..1 fraction of OpenClaw/handback provenance fields present (aligned with bot/core staging keys)."""
    has_source = bool(re.search(r"^candidate_source:\s*\S", yaml_body, re.MULTILINE))
    has_path = bool(re.search(r"^artifact_path:\s*\S", yaml_body, re.MULTILINE))
    has_sha = bool(re.search(r"^artifact_sha256:\s*\S", yaml_body, re.MULTILINE))
    has_receipt = bool(re.search(r"^continuity_receipt_path:\s*\S", yaml_body, re.MULTILINE))
    has_const = bool(
        re.search(r"^constitution_check_status:\s*\S", yaml_body, re.MULTILINE)
        or re.search(r"^constitution_rule_ids:\s*\S", yaml_body, re.MULTILINE)
    )
    parts = [has_source, has_path, has_sha, has_receipt, has_const]
    return sum(1 for x in parts if x) / len(parts)


def mean_pending_provenance_score(full_md: str) -> float | None:
    """Mean provenance score over pending YAML blobs; None if no pending candidates."""
    blobs = iter_pending_yaml_blobs(full_md)
    if not blobs:
        return None
    return sum(yaml_blob_provenance_fraction(b) for b in blobs) / len(blobs)


def mean_pending_provenance_from_path(gate_path: Path) -> float | None:
    if not gate_path.is_file():
        return None
    return mean_pending_provenance_score(gate_path.read_text(encoding="utf-8"))


def sweep_rejected_to_processed(gate_path: Path) -> list[str]:
    """Move rejected candidates from the active section to Processed. Returns ids moved."""
    if not gate_path.is_file():
        return []
    content = gate_path.read_text(encoding="utf-8")
    active, _processed = split_gate_sections(content)
    moved: list[str] = []
    for m in CANDIDATE_BLOCK_RE.finditer(active):
        cid = m.group(1)
        yaml_body = m.group(3)
        if re.search(r"^status:\s*rejected\s*$", yaml_body, re.MULTILINE):
            moved.append(cid)
    if not moved:
        return []
    for cid in moved:
        block_re = re.compile(
            rf"^### {re.escape(cid)}(?:\s*\([^)]*\))?\s*\n```yaml\n.*?```\n?",
            re.MULTILINE | re.DOTALL,
        )
        match = block_re.search(content)
        if not match:
            continue
        block_text = match.group(0)
        content = content.replace(block_text, "", 1)
        marker = re.search(r"^## Processed\s*$", content, re.MULTILINE)
        if marker:
            insert_at = marker.end()
            content = content[:insert_at] + "\n\n" + block_text + content[insert_at:]
        else:
            content = content.rstrip() + "\n\n## Processed\n\n" + block_text
    content = re.sub(r"\n{3,}", "\n\n", content)
    gate_path.write_text(content, encoding="utf-8")
    return moved


__all__ = [
    "CANDIDATE_BLOCK_RE",
    "iter_candidate_yaml_blocks",
    "iter_pending_yaml_blobs",
    "mean_pending_provenance_from_path",
    "mean_pending_provenance_score",
    "pending_candidates_region",
    "split_gate_sections",
    "sweep_rejected_to_processed",
    "yaml_blob_provenance_fraction",
]

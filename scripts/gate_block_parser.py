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
    """Slice between ## Candidates and ## Processed (dashboard / metrics alignment)."""
    idx_c = full_md.find("## Candidates")
    idx_p = full_md.find("## Processed")
    if idx_c >= 0 and idx_p > idx_c:
        return full_md[idx_c:idx_p]
    if idx_c >= 0:
        return full_md[idx_c:]
    return ""


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


__all__ = [
    "CANDIDATE_BLOCK_RE",
    "iter_candidate_yaml_blocks",
    "iter_pending_yaml_blobs",
    "mean_pending_provenance_from_path",
    "mean_pending_provenance_score",
    "pending_candidates_region",
    "split_gate_sections",
    "yaml_blob_provenance_fraction",
]

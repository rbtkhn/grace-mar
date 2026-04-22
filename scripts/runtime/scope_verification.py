"""
Worker-verified scope metrics for execution receipts (runtime-only, non-canonical).

Verified traversal counts are measured in-code; any ``stated_coverage`` from proposal
text is regex-extracted and not trusted as proof of filesystem access.
"""

from __future__ import annotations

import re
from typing import Any, Literal

PATHS_SAMPLE_MAX = 20

StatedSource = Literal["proposal_regex", "absent", "parse_failed"]


def parse_stated_file_count_from_proposal(text: str) -> tuple[int | None, StatedSource]:
    """
    Extract optional 'files listed' line from worker-generated proposal markdown.
    Returns (files_claimed, source). Does not assert truth — narrative extract only.
    """
    m = re.search(r"\*\*files listed:\*\*\s*(\d+)", text, re.IGNORECASE)
    if m:
        return int(m.group(1)), "proposal_regex"
    m2 = re.search(r"files\s+listed:.*?\*?\*?\s*(\d+)", text, re.IGNORECASE)
    if m2:
        return int(m2.group(1)), "proposal_regex"
    return None, "absent"


def compute_coverage_status(
    *,
    files_opened: int,
    files_seen: int,
    files_claimed: int | None,
    stated_source: str,
) -> tuple[float | None, str, list[str]]:
    """
    Return (coverage_ratio, status, extra_warnings). Ratio null when comparison undefined.
    """
    w: list[str] = []
    if files_claimed is None or stated_source == "absent":
        return None, "unstated", w
    if files_claimed == files_opened:
        return 1.0, "aligned", w
    r = min(1.0, float(files_opened) / max(1, files_claimed))
    if files_claimed > files_opened:
        w.append(
            f"stated file count ({files_claimed}) exceeds opened count ({files_opened}) — overclaim"
        )
        return round(r, 3), "overclaim_suspected", w
    w.append(
        f"stated file count ({files_claimed}) is below opened count ({files_opened}) — underclaim"
    )
    return round(r, 3), "underclaim_suspected", w


def build_scope_verification_block(
    *,
    files_seen: int,
    rel_paths: list[str],
    files_opened: int,
    chunks_read: int,
    proposal_body: str,
    base_warnings: list[str],
) -> dict[str, Any]:
    """Assemble the scope_verification object for execution-receipt.v1."""
    files_claimed, src = parse_stated_file_count_from_proposal(proposal_body)
    stated: dict[str, Any] = {
        "files_claimed": files_claimed,
        "source": src,
    }
    ratio, status, extra = compute_coverage_status(
        files_opened=files_opened,
        files_seen=files_seen,
        files_claimed=files_claimed,
        stated_source=src,  # type: ignore[arg-type]
    )
    warnings = list(base_warnings) + extra
    return {
        "traversal": {
            "files_seen": files_seen,
            "files_opened": files_opened,
            "chunks_read": chunks_read,
            "paths_sample": rel_paths[:PATHS_SAMPLE_MAX],
        },
        "stated_coverage": stated,
        "coverage_ratio": ratio,
        "status": status,
        "warnings": warnings,
    }

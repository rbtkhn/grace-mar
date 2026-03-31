"""Correlate audit rows with gate candidates, bundles, and merge batches."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any


def filter_pipeline_by_candidate(rows: list[dict[str, Any]], candidate_id: str) -> list[dict[str, Any]]:
    cid = candidate_id.strip().upper()
    return [r for r in rows if str(r.get("candidate_id") or "").upper() == cid]


def filter_harness(rows: list[dict[str, Any]], candidate_id: str, bundle_id: str | None) -> list[dict[str, Any]]:
    cid = candidate_id.strip().upper() if candidate_id else ""
    out: list[dict[str, Any]] = []
    for r in rows:
        if bundle_id and str(r.get("bundle_id") or "") == bundle_id:
            out.append(r)
            continue
        if cid:
            if str(r.get("candidate_id") or "").upper() == cid:
                out.append(r)
                continue
            cids = r.get("candidate_ids")
            if isinstance(cids, list) and any(str(x).upper() == cid for x in cids):
                out.append(r)
    return out


def filter_merge_receipts(rows: list[dict[str, Any]], candidate_id: str) -> list[dict[str, Any]]:
    cid = candidate_id.strip().upper()
    out: list[dict[str, Any]] = []
    for r in rows:
        ids = r.get("candidate_ids")
        if isinstance(ids, list) and any(str(x).upper() == cid for x in ids):
            out.append(r)
    return out


def find_pipeline_row_by_event_id(rows: list[dict[str, Any]], event_id: str) -> dict[str, Any] | None:
    want = event_id.strip()
    for r in rows:
        if str(r.get("event_id") or "") == want:
            return r
    return None


def harness_rows_for_event_id(hv: list[dict[str, Any]], eid: str) -> list[dict[str, Any]]:
    want = eid.strip()
    out: list[dict[str, Any]] = []
    for r in hv:
        if str(r.get("event_id") or "") == want:
            out.append(r)
            continue
        apl = r.get("applied_pipeline_event_ids")
        if isinstance(apl, list) and want in [str(x) for x in apl]:
            out.append(r)
            continue
        spl = r.get("staged_parent_event_ids")
        if isinstance(spl, list) and want in [str(x) for x in spl]:
            out.append(r)
    return out


def find_candidate_yaml(gate_text: str, candidate_id: str) -> str | None:
    want = candidate_id.strip().upper()
    for m in re.finditer(
        r"### (CANDIDATE-\d+)(?:\s*\(([^)]*)\))?\s*\n```yaml\n(.*?)```",
        gate_text,
        re.DOTALL,
    ):
        if m.group(1).upper() == want:
            return m.group(3).strip()
    return None


def evidence_snippet(evidence_path: Path, evidence_id: str) -> str | None:
    if not evidence_path.is_file():
        return None
    text = evidence_path.read_text(encoding="utf-8", errors="ignore")
    for line in text.splitlines():
        if evidence_id.upper() in line.upper() and "ACT-" in line:
            return line.strip()[:500]
    return None


def transcript_hint(transcript_path: Path, max_lines: int = 40) -> str:
    if not transcript_path.is_file():
        return ""
    lines = transcript_path.read_text(encoding="utf-8", errors="ignore").splitlines()
    tail = lines[-max_lines:] if len(lines) > max_lines else lines
    return "\n".join(tail)


__all__ = [
    "evidence_snippet",
    "filter_harness",
    "filter_merge_receipts",
    "filter_pipeline_by_candidate",
    "find_candidate_yaml",
    "find_pipeline_row_by_event_id",
    "harness_rows_for_event_id",
    "transcript_hint",
]

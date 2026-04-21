#!/usr/bin/env python3
"""
Structured review model for RECURSION-GATE candidates.

This module keeps recursion-gate.md as the single source of truth while
providing derived fields for review surfaces such as dashboards and inboxes.
"""

from __future__ import annotations

import json
import logging
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

try:
    from recursion_gate_territory import (
        TERRITORY_LABEL_WORK_POLITICS,
        TERRITORY_WORK_POLITICS,
        channel_key_is_work_politics,
        normalize_territory_cli,
        territory_from_yaml_block,
    )
except ImportError:
    from scripts.recursion_gate_territory import (
        TERRITORY_LABEL_WORK_POLITICS,
        TERRITORY_WORK_POLITICS,
        channel_key_is_work_politics,
        normalize_territory_cli,
        territory_from_yaml_block,
    )
try:
    from identity_library_boundary_rules import gate_suggested_reference_surface
except ImportError:
    from scripts.identity_library_boundary_rules import gate_suggested_reference_surface

try:
    from repo_io import read_path, REPO_ROOT, profile_dir, DEFAULT_USER_ID
except ImportError:
    from scripts.repo_io import read_path, REPO_ROOT, profile_dir, DEFAULT_USER_ID

try:
    from gate_block_parser import (
        iter_candidate_yaml_blocks,
        pending_candidates_region,
        split_gate_sections,
    )
except ImportError:
    from scripts.gate_block_parser import (
        iter_candidate_yaml_blocks,
        pending_candidates_region,
        split_gate_sections,
    )

_read = read_path
_profile_dir = profile_dir
DEFAULT_USER = DEFAULT_USER_ID


def _fork_dir(user_id: str, repo_root: Path | None) -> Path:
    """Users/<user_id> under repo (defaults to ``_profile_dir`` / REPO_ROOT)."""
    if repo_root is None:
        return _profile_dir(user_id)
    return repo_root.resolve() / "users" / user_id

_STOPWORDS = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "be",
    "because",
    "for",
    "from",
    "has",
    "in",
    "is",
    "it",
    "its",
    "of",
    "on",
    "or",
    "that",
    "the",
    "their",
    "this",
    "to",
    "with",
    "you",
    "your",
}


def _strip_quotes(value: str) -> str:
    return value.strip().strip("\"'")


def _normalize(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", (text or "").lower()).strip()


def _meaningful_keywords(text: str) -> list[str]:
    words = []
    for word in _normalize(text).split():
        if len(word) < 4 or word in _STOPWORDS:
            continue
        words.append(word)
    return words


def _extract_scalar(yaml_body: str, key: str) -> str:
    m = re.search(rf"^{re.escape(key)}:\s*(.+)$", yaml_body, re.MULTILINE)
    if not m:
        return ""
    return _strip_quotes(m.group(1))


def _reflection_gate_label(impact_tier_raw: str) -> str:
    """Reflection Gates v1 label from author impact_tier: none | light | heavy."""
    s = (impact_tier_raw or "").strip().lower()
    if s == "medium":
        return "light"
    if s in ("high", "boundary"):
        return "heavy"
    return "none"


def _extract_block(yaml_body: str, key: str) -> str:
    lines = yaml_body.splitlines()
    out: list[str] = []
    start_idx: int | None = None
    base_indent = 0
    for idx, line in enumerate(lines):
        match = re.match(rf"^(\s*){re.escape(key)}:\s*(.*)$", line)
        if not match:
            continue
        tail = match.group(2).strip()
        if tail:
            return _strip_quotes(tail)
        start_idx = idx + 1
        base_indent = len(match.group(1))
        break
    if start_idx is None:
        return ""
    for line in lines[start_idx:]:
        if not line.strip():
            if out:
                out.append("")
            continue
        indent = len(line) - len(line.lstrip(" "))
        if indent <= base_indent and re.match(r"^\s*[A-Za-z0-9_-]+:", line):
            break
        out.append(line[base_indent + 2 :] if indent >= base_indent + 2 else line.strip())
    return "\n".join(out).strip()


def _parse_candidates_metrics_shape(section: str) -> list[dict]:
    """Parse a gate section into list of dicts with id, status, outcome (for metrics)."""
    result: list[dict] = []
    current: dict | None = None
    for line in section.splitlines():
        m = re.match(r"^### (CANDIDATE-\d+)", line)
        if m:
            current = {"id": m.group(1)}
            result.append(current)
            continue
        if current is not None and line.strip().startswith("status:"):
            status = line.split(":", 1)[1].strip().lower()
            current["status"] = status
            if "approved" in status or "rejected" in status:
                current["outcome"] = "approved" if "approved" in status else "rejected"
    return result


def parse_gate_for_metrics(content: str) -> tuple[list[dict], list[dict]]:
    """
    Parse recursion-gate content into (pending_list, processed_list) for pipeline health.
    Each item has id, status, and outcome when present. Use from metrics.py.
    """
    processed_tail = split_gate_sections(content)[1]
    pending_section = pending_candidates_region(content)
    processed_section = processed_tail
    pending = _parse_candidates_metrics_shape(pending_section)
    processed = _parse_candidates_metrics_shape(processed_section)
    return pending, processed


def _parse_candidates_dashboard_shape(section: str) -> list[dict]:
    """Parse pending section into list of {id, summary, mind_category, priority_score} for dashboard/profile."""
    result: list[dict] = []
    for cid, _title, yaml_body in iter_candidate_yaml_blocks(section):
        result.append({
            "id": cid,
            "summary": _extract_scalar(yaml_body, "summary").strip().strip('"'),
            "mind_category": _extract_scalar(yaml_body, "mind_category").strip(),
            "priority_score": _extract_scalar(yaml_body, "priority_score").strip(),
        })
    return result


def parse_gate_pending_for_dashboard(content: str) -> tuple[int, list[dict]]:
    """
    Parse recursion-gate content into (pending_count, pending_candidates) for profile/dashboard.
    Each candidate has id, summary, mind_category, priority_score. Use from generate_profile.py.
    """
    pending_section = pending_candidates_region(content)
    candidates = _parse_candidates_dashboard_shape(pending_section)
    return len(candidates), candidates


def _parse_timestamp(raw_ts: str) -> datetime | None:
    if not raw_ts:
        return None
    raw_ts = raw_ts.strip()
    try:
        if len(raw_ts) == 10:
            return datetime.strptime(raw_ts, "%Y-%m-%d").replace(tzinfo=timezone.utc)
        if "T" in raw_ts:
            dt = datetime.fromisoformat(raw_ts.replace("Z", "+00:00"))
            return dt if dt.tzinfo else dt.replace(tzinfo=timezone.utc)
        return datetime.strptime(raw_ts[:19], "%Y-%m-%d %H:%M:%S").replace(tzinfo=timezone.utc)
    except ValueError:
        return None


def _age_days(raw_ts: str) -> int | None:
    dt = _parse_timestamp(raw_ts)
    if not dt:
        return None
    return max(0, (datetime.now(timezone.utc) - dt).days)


def _pipeline_events_index(user_id: str, *, repo_root: Path | None = None) -> dict[str, list[dict]]:
    """
    Single read of pipeline-events.jsonl: map candidate_id -> last 8 events (chronological order).
    Used by parse_review_candidates once per call instead of O(candidates × file_size).
    """
    events_path = _fork_dir(user_id, repo_root) / "pipeline-events.jsonl"
    if not events_path.exists():
        return {}
    by_cid: dict[str, list[dict]] = {}
    for line in events_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError:
            continue
        if not isinstance(row, dict):
            continue
        cid = row.get("candidate_id")
        if not cid:
            continue
        by_cid.setdefault(str(cid), []).append(row)
    return {cid: rows[-8:] for cid, rows in by_cid.items()}


def _pipeline_events_for_candidate(user_id: str, candidate_id: str) -> list[dict]:
    """Last 8 pipeline events for one candidate (reads index built from full file once)."""
    return _pipeline_events_index(user_id).get(candidate_id, [])


def _has_advisory_flagged(events: list[dict]) -> bool:
    for row in reversed(events):
        if row.get("event") == "intent_constitutional_critique":
            return str(row.get("status") or "").lower() == "advisory_flagged"
    return False


def _duplicate_hints(candidate: dict, self_text: str) -> list[str]:
    hints: list[str] = []
    summary = candidate.get("summary", "")
    lower_summary = summary.lower()
    if any(marker in lower_summary for marker in ("duplicate", "overlap", "already in record", "already in ix", "skip prompt")):
        hints.append(summary)
    for key in ("suggested_entry", "prompt_addition"):
        value = str(candidate.get(key) or "").strip()
        if not value or value.lower() == "none":
            continue
        normalized = _normalize(value)
        if len(normalized) > 24 and normalized in _normalize(self_text):
            hints.append(f"{key} overlaps existing Record text")
            continue
        keywords = _meaningful_keywords(value)
        if keywords:
            overlap = sum(1 for keyword in keywords[:5] if keyword in _normalize(self_text))
            if overlap >= 3:
                hints.append(f"{key} likely overlaps existing Record knowledge/personality")
    seen = set()
    deduped: list[str] = []
    for hint in hints:
        if hint in seen:
            continue
        seen.add(hint)
        deduped.append(hint)
    return deduped[:3]


def _territory_label(territory: str, channel_key: str, proposal_class: str,
                     signal_type: str) -> str:
    if territory == TERRITORY_WORK_POLITICS:
        return TERRITORY_LABEL_WORK_POLITICS
    pc_up = (proposal_class or "").upper()
    st_low = (signal_type or "").lower()
    ch_low = (channel_key or "").lower()
    if pc_up.startswith("CIV_MEM") or st_low == "civilizational_insight" or "cmc-ingest" in ch_low:
        return "CIV-MEM"
    return "Companion"


def _cmc_source_provenance(row: dict) -> dict | None:
    """Extract CMC provenance metadata when the candidate originated from CMC ingest."""
    ch = (row.get("channel_key") or "").lower()
    st = (row.get("signal_type") or "").lower()
    pc = (row.get("proposal_class") or "").upper()
    if not ("cmc" in ch or st == "civilizational_insight" or pc.startswith("CIV_MEM")):
        return None
    source = row.get("source") or ""
    return {
        "is_cmc": True,
        "ingest_channel": row.get("channel_key", ""),
        "scholar_source": source if "SCHOLAR" in source else None,
        "target_surface": "SELF-LIBRARY/CIV-MEM",
        "epistemic_note": "CMC material is reference, not identity. Treat as interpretation unless independently verified.",
    }


def _risk_tier(candidate: dict) -> str:
    if candidate["has_conflict_markers"] or candidate["advisory_flagged"] or candidate["duplicate_hints"]:
        return "manual_escalate"
    if candidate["ready_for_quick_merge"]:
        return "quick_merge_eligible"
    return "review_batch"


def _compute_boundary_review(row: dict) -> dict:
    """
    Boundary Review Queue hints: target surface vs heuristic suggestion.
    Does not block merge — companion still approves. See docs/boundary-review-queue.md.
    """
    territory = row.get("territory") or ""
    ch = (row.get("channel_key") or "").lower()
    if territory == TERRITORY_WORK_POLITICS or channel_key_is_work_politics(ch) or "work-political" in ch:
        return {
            "target_surface": "WORK-LAYER",
            "suggested_surface": "WORK-LAYER",
            "misfiled_warning": None,
            "hint_reasons": [],
            "confidence": "high",
        }

    pc = (row.get("proposal_class") or "SELF_KNOWLEDGE_ADD").upper()
    text = " ".join(
        x
        for x in (
            row.get("summary") or "",
            (row.get("suggested_entry") or "")[:1500],
            (row.get("example_from_exchange") or "")[:800],
        )
        if x
    )

    if pc.startswith("CIV_MEM"):
        return {
            "target_surface": "CIV-MEM",
            "suggested_surface": "CIV-MEM",
            "misfiled_warning": None,
            "hint_reasons": ["proposal_class is CIV-MEM_*"],
            "confidence": "high",
        }
    if pc.startswith("SELF_LIBRARY"):
        return {
            "target_surface": "SELF-LIBRARY",
            "suggested_surface": "SELF-LIBRARY",
            "misfiled_warning": None,
            "hint_reasons": ["proposal_class is SELF_LIBRARY_*"],
            "confidence": "high",
        }

    target = "SELF-KNOWLEDGE"
    suggested = "SELF-KNOWLEDGE"
    reasons: list[str] = []
    surf, surf_reasons = gate_suggested_reference_surface(text)
    if surf:
        suggested = surf
        reasons.extend(surf_reasons)

    misfiled = None
    if suggested != "SELF-KNOWLEDGE":
        misfiled = (
            f"Target surface is {target} but content suggests {suggested}. "
            "Misfiled? Consider CIV_MEM_* or SELF_LIBRARY_* on the gate YAML, or reject."
        )

    return {
        "target_surface": target,
        "suggested_surface": suggested,
        "misfiled_warning": misfiled,
        "hint_reasons": reasons,
        "confidence": "low" if misfiled else ("medium" if reasons else "high"),
    }


def _try_persist_boundary_classification(user_id: str, row: dict) -> None:
    """Write review-queue/boundary-classifications/<id>.json when grace_mar is importable."""
    root = Path(__file__).resolve().parents[1]
    src = root / "src"
    if src.is_dir() and str(src) not in sys.path:
        sys.path.insert(0, str(src))
    try:
        from grace_mar.merge.boundary_classifier import sync_boundary_classification_artifact

        sync_boundary_classification_artifact(user_id, row, repo_root=root)
    except Exception as exc:
        logging.getLogger(__name__).warning("boundary classification persist failed: %s", exc)


def _ready_for_quick_merge(candidate: dict) -> bool:
    if candidate.get("status") != "pending":
        return False
    if candidate["has_multi_target"] or candidate["has_conflict_markers"] or candidate["advisory_flagged"]:
        return False
    profile_target = candidate.get("profile_target", "")
    if not re.match(r"^IX-[ABC]\.", profile_target):
        return False
    return True


def parse_review_candidates(user_id: str = DEFAULT_USER, *, repo_root: Path | None = None) -> list[dict]:
    gate_path = _fork_dir(user_id, repo_root) / "recursion-gate.md"
    self_path = _fork_dir(user_id, repo_root) / "self.md"
    content = _read(gate_path)
    self_text = _read(self_path)
    pipeline_by_candidate = _pipeline_events_index(user_id, repo_root=repo_root)
    active, _ = split_gate_sections(content)
    rows: list[dict] = []
    for candidate_id, title, yaml_body in iter_candidate_yaml_blocks(active):
        status = _extract_scalar(yaml_body, "status") or "pending"
        channel_key = _extract_scalar(yaml_body, "channel_key")
        timestamp = _extract_scalar(yaml_body, "timestamp")
        territory = territory_from_yaml_block(yaml_body)
        prompt_addition = _extract_block(yaml_body, "prompt_addition")
        profile_target = _extract_scalar(yaml_body, "profile_target")
        prompt_section = _extract_scalar(yaml_body, "prompt_section")
        events = pipeline_by_candidate.get(candidate_id, [])
        raw_pc = (_extract_scalar(yaml_body, "proposal_class") or "").strip()
        if raw_pc:
            eff_pc, pc_inferred = raw_pc, False
        else:
            mc = (_extract_scalar(yaml_body, "mind_category") or "").lower()
            if mc == "knowledge":
                eff_pc = "SELF_KNOWLEDGE_ADD"
            elif mc == "curiosity":
                eff_pc = "SELF_KNOWLEDGE_ADD"
            elif mc == "personality":
                eff_pc = "SELF_KNOWLEDGE_ADD"
            else:
                eff_pc = "SELF_KNOWLEDGE_ADD"
            pc_inferred = True
        row = {
            "id": candidate_id,
            "title": title,
            "status": status,
            "timestamp": timestamp,
            "age_days": _age_days(timestamp),
            "channel_key": channel_key,
            "territory": territory,
            "territory_label": _territory_label(territory, channel_key, eff_pc,
                                                _extract_scalar(yaml_body, "signal_type")),
            "proposal_class": eff_pc,
            "proposal_class_raw": raw_pc or None,
            "proposal_class_inferred": pc_inferred,
            "source": _extract_scalar(yaml_body, "source"),
            "candidate_source": _extract_scalar(yaml_body, "candidate_source"),
            "origin": _extract_scalar(yaml_body, "origin"),
            "lineage_class": _extract_scalar(yaml_body, "lineage_class"),
            "session_id": _extract_scalar(yaml_body, "session_id"),
            "operator_source": _extract_scalar(yaml_body, "operator_source"),
            "artifact_path": _extract_scalar(yaml_body, "artifact_path"),
            "artifact_sha256": _extract_scalar(yaml_body, "artifact_sha256"),
            "constitution_check_status": _extract_scalar(yaml_body, "constitution_check_status"),
            "constitution_rule_ids": _extract_scalar(yaml_body, "constitution_rule_ids"),
            "mind_category": _extract_scalar(yaml_body, "mind_category"),
            "signal_type": _extract_scalar(yaml_body, "signal_type"),
            "priority_score": _extract_scalar(yaml_body, "priority_score"),
            "summary": _extract_scalar(yaml_body, "summary"),
            "profile_target": profile_target,
            "example_from_exchange": _extract_block(yaml_body, "example_from_exchange"),
            "source_exchange": _extract_block(yaml_body, "source_exchange"),
            "suggested_entry": _extract_block(yaml_body, "suggested_entry"),
            "prompt_section": prompt_section,
            "prompt_addition": prompt_addition,
            "suggested_followup": _extract_block(yaml_body, "suggested_followup"),
            "raw_block": yaml_body,
            "has_conflict_markers": bool(re.search(r"conflicts?:|contradiction|advisory_flagged", yaml_body, re.IGNORECASE)),
            "has_prompt_change": bool(prompt_addition and prompt_addition.lower() != "none"),
            "has_multi_target": ("," in profile_target) or ("," in prompt_section) or (" / " in prompt_section),
            "has_artifact_payload": bool(re.search(r"artifacts?:|artifact_path:|image_file:|create_entries:", yaml_body, re.IGNORECASE)),
            "audit_trail": [
                {
                    "event": row.get("event"),
                    "ts": row.get("ts"),
                    "status": row.get("status"),
                    "reason": row.get("reason") or row.get("rejection_reason"),
                }
                for row in events
            ],
            "advisory_flagged": _has_advisory_flagged(events),
            "impact_tier": _extract_scalar(yaml_body, "impact_tier"),
            "envelope_class": _extract_scalar(yaml_body, "envelope_class"),
            "reflection_ack": _extract_scalar(yaml_body, "reflection_ack"),
        }
        row["duplicate_hints"] = _duplicate_hints(row, self_text)
        row["ready_for_quick_merge"] = _ready_for_quick_merge(row) and not row["duplicate_hints"]
        row["risk_tier"] = _risk_tier(row)
        row["reflection_gate"] = _reflection_gate_label(row.get("impact_tier") or "")
        row["boundary_review"] = _compute_boundary_review(row)
        row["cmc_source_provenance"] = _cmc_source_provenance(row)
        _try_persist_boundary_classification(user_id, row)
        rows.append(row)
    rows.sort(key=lambda row: row.get("timestamp", ""), reverse=True)
    return rows


def get_review_candidate(user_id: str, candidate_id: str) -> dict | None:
    for row in parse_review_candidates(user_id=user_id):
        if row["id"] == candidate_id:
            return row
    return None


def filter_review_candidates(
    rows: list[dict],
    *,
    status: str = "",
    risk_tier: str = "",
    territory: str = "",
    signal_type: str = "",
    proposal_class_substr: str = "",
) -> list[dict]:
    out = rows
    if status:
        out = [row for row in out if row.get("status") == status]
    if risk_tier:
        out = [row for row in out if row.get("risk_tier") == risk_tier]
    if signal_type:
        st = signal_type.strip().lower()
        out = [row for row in out if (row.get("signal_type") or "").strip().lower() == st]
    if proposal_class_substr:
        pcs = proposal_class_substr.strip().lower()
        out = [
            row
            for row in out
            if pcs
            in f"{row.get('proposal_class_raw') or ''} {row.get('proposal_class') or ''}".lower()
        ]
    if territory and territory != "all":
        territory = normalize_territory_cli(territory)
        if territory == "companion":
            out = [row for row in out if row.get("territory") != TERRITORY_WORK_POLITICS]
        elif territory == "work-politics":
            out = [row for row in out if row.get("territory") == TERRITORY_WORK_POLITICS]
        else:
            out = [row for row in out if row.get("territory") == territory]
    return out


__all__ = [
    "DEFAULT_USER",
    "filter_review_candidates",
    "get_review_candidate",
    "parse_gate_for_metrics",
    "parse_review_candidates",
    "split_gate_sections",
]

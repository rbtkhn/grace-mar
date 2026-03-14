#!/usr/bin/env python3
"""
Structured review model for RECURSION-GATE candidates.

This module keeps recursion-gate.md as the single source of truth while
providing derived fields for review surfaces such as dashboards and inboxes.
"""

from __future__ import annotations

import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path

try:
    from recursion_gate_territory import TERRITORY_WAP, territory_from_yaml_block
except ImportError:
    from scripts.recursion_gate_territory import TERRITORY_WAP, territory_from_yaml_block

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_USER = os.getenv("GRACE_MAR_USER_ID", "grace-mar").strip() or "grace-mar"

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


def _profile_dir(user_id: str) -> Path:
    return REPO_ROOT / "users" / user_id


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


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


def _candidate_matches(full_md: str) -> list[re.Match[str]]:
    active, _processed = split_gate_sections(full_md)
    return list(
        re.finditer(
            r"### (CANDIDATE-\d+)(?:\s*\(([^)]*)\))?\s*\n```yaml\n(.*?)```",
            active,
            re.DOTALL,
        )
    )


def split_gate_sections(full_md: str) -> tuple[str, str]:
    """
    Split at the actual `## Processed` heading, not header prose mentioning it.
    Returns (active_section, processed_section_without_heading).
    """
    marker = re.search(r"^## Processed\s*$", full_md, re.MULTILINE)
    if not marker:
        return full_md, ""
    return full_md[: marker.start()], full_md[marker.end() :]


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


def _pipeline_events_for_candidate(user_id: str, candidate_id: str) -> list[dict]:
    events_path = _profile_dir(user_id) / "pipeline-events.jsonl"
    if not events_path.exists():
        return []
    events: list[dict] = []
    for line in events_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError:
            continue
        if not isinstance(row, dict) or row.get("candidate_id") != candidate_id:
            continue
        events.append(row)
    return events[-8:]


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


def _risk_tier(candidate: dict) -> str:
    if candidate["has_conflict_markers"] or candidate["advisory_flagged"] or candidate["duplicate_hints"]:
        return "manual_escalate"
    if candidate["ready_for_quick_merge"]:
        return "quick_merge_eligible"
    return "review_batch"


def _ready_for_quick_merge(candidate: dict) -> bool:
    if candidate.get("status") != "pending":
        return False
    if candidate["has_multi_target"] or candidate["has_conflict_markers"] or candidate["advisory_flagged"]:
        return False
    profile_target = candidate.get("profile_target", "")
    if not re.match(r"^IX-[ABC]\.", profile_target):
        return False
    return True


def parse_review_candidates(user_id: str = DEFAULT_USER) -> list[dict]:
    gate_path = _profile_dir(user_id) / "recursion-gate.md"
    self_path = _profile_dir(user_id) / "self.md"
    content = _read(gate_path)
    self_text = _read(self_path)
    rows: list[dict] = []
    for match in _candidate_matches(content):
        candidate_id = match.group(1)
        title = (match.group(2) or "").strip()
        yaml_body = match.group(3)
        status = _extract_scalar(yaml_body, "status") or "pending"
        channel_key = _extract_scalar(yaml_body, "channel_key")
        timestamp = _extract_scalar(yaml_body, "timestamp")
        territory = territory_from_yaml_block(yaml_body)
        prompt_addition = _extract_block(yaml_body, "prompt_addition")
        profile_target = _extract_scalar(yaml_body, "profile_target")
        prompt_section = _extract_scalar(yaml_body, "prompt_section")
        events = _pipeline_events_for_candidate(user_id, candidate_id)
        row = {
            "id": candidate_id,
            "title": title,
            "status": status,
            "timestamp": timestamp,
            "age_days": _age_days(timestamp),
            "channel_key": channel_key,
            "territory": territory,
            "territory_label": "WAP" if territory == TERRITORY_WAP else "Companion",
            "source": _extract_scalar(yaml_body, "source"),
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
        }
        row["duplicate_hints"] = _duplicate_hints(row, self_text)
        row["ready_for_quick_merge"] = _ready_for_quick_merge(row) and not row["duplicate_hints"]
        row["risk_tier"] = _risk_tier(row)
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
) -> list[dict]:
    out = rows
    if status:
        out = [row for row in out if row.get("status") == status]
    if risk_tier:
        out = [row for row in out if row.get("risk_tier") == risk_tier]
    if territory:
        if territory == "companion":
            out = [row for row in out if row.get("territory") != TERRITORY_WAP]
        else:
            out = [row for row in out if row.get("territory") == territory]
    return out


__all__ = [
    "DEFAULT_USER",
    "filter_review_candidates",
    "get_review_candidate",
    "parse_review_candidates",
    "split_gate_sections",
]

#!/usr/bin/env python3
"""
Pipeline health and trust metrics for Grace-Mar.

Aligns with white paper Appendix B and DESIGN-NOTES key metrics:
  - Pipeline health (stale candidates, approval rate)
  - Record completeness (IX counts)
  - Trust signal (approval vs rejection)

Mitigates "user fatigue" risk by flagging bottlenecks.
"""

import json
import re
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
PROFILE_DIR = REPO_ROOT / "users" / "grace-mar"
STALE_DAYS = 7


def _read(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8")


@dataclass
class PipelineHealth:
    stale_candidates: int
    pending_count: int
    approval_rate: float | None
    rejection_rate: float | None
    applied_total: int
    rejected_total: int
    last_applied_ts: str | None
    days_since_last_activity: float | None


@dataclass
class RecordCompleteness:
    ix_a: int
    ix_b: int
    ix_c: int
    total_ix: int


@dataclass
class IntentDrift:
    total_conflicts: int
    conflicts_by_source: dict[str, int]
    conflicts_by_rule: dict[str, int]
    rejection_categories: dict[str, int]


def parse_pending_review(content: str) -> tuple[list[dict], list[dict]]:
    """
    Extract pending and processed candidates from PENDING-REVIEW.md.
    Returns (pending_list, processed_list).
    """
    pending = []
    processed = []
    in_candidates = False
    in_processed = False
    current: dict | None = None

    for line in content.splitlines():
        if line.strip() == "## Candidates":
            in_candidates = True
            in_processed = False
            continue
        if line.strip() == "## Processed":
            in_candidates = False
            in_processed = True
            continue

        m = re.match(r"^### (CANDIDATE-\d+)", line)
        if m:
            current_id = m.group(1)
            current = {"id": current_id}
            if in_candidates:
                pending.append(current)
            elif in_processed:
                processed.append(current)
            continue

        if current is not None and line.strip().startswith("status:"):
            status = line.split(":", 1)[1].strip().lower()
            current["status"] = status
            if "approved" in status or "rejected" in status:
                current["outcome"] = "approved" if "approved" in status else "rejected"

    return pending, processed


def compute_pipeline_health() -> PipelineHealth:
    """Compute pipeline health from PENDING-REVIEW and PIPELINE-EVENTS."""
    pr_content = _read(PROFILE_DIR / "PENDING-REVIEW.md")
    pending, processed = parse_pending_review(pr_content)

    pr_path = PROFILE_DIR / "PENDING-REVIEW.md"
    mtime = datetime.fromtimestamp(pr_path.stat().st_mtime) if pr_path.exists() else None
    now = datetime.now()
    stale_candidates = 0
    if mtime and pending:
        days_old = (now - mtime).total_seconds() / 86400
        if days_old >= STALE_DAYS:
            stale_candidates = len(pending)

    approved = sum(1 for p in processed if p.get("outcome") == "approved")
    rejected = sum(1 for p in processed if p.get("outcome") == "rejected")
    total_processed = approved + rejected
    approval_rate = approved / total_processed if total_processed else None
    rejection_rate = rejected / total_processed if total_processed else None

    events_path = PROFILE_DIR / "PIPELINE-EVENTS.jsonl"
    applied_total = rejected_total = 0
    last_applied_ts = None
    if events_path.exists():
        for line in events_path.read_text().strip().splitlines():
            if not line:
                continue
            try:
                row = json.loads(line)
                e = row.get("event", "")
                ts = row.get("ts", "")
                if e in ("applied", "approved"):
                    applied_total += 1
                    if ts:
                        last_applied_ts = ts
                elif e == "rejected":
                    rejected_total += 1
            except json.JSONDecodeError:
                pass

    days_since = None
    if last_applied_ts:
        try:
            dt = datetime.fromisoformat(last_applied_ts.replace("Z", "+00:00"))
            if dt.tzinfo:
                dt = dt.replace(tzinfo=None)
            days_since = (now - dt).total_seconds() / 86400
        except (ValueError, TypeError):
            pass

    return PipelineHealth(
        stale_candidates=stale_candidates,
        pending_count=len(pending),
        approval_rate=approval_rate,
        rejection_rate=rejection_rate,
        applied_total=applied_total,
        rejected_total=rejected_total,
        last_applied_ts=last_applied_ts,
        days_since_last_activity=days_since,
    )


def compute_record_completeness() -> RecordCompleteness:
    """IX channel counts from SELF.md."""
    content = _read(PROFILE_DIR / "SELF.md")
    ix_a = len(re.findall(r"id:\s+LEARN-\d+", content))
    ix_b = len(re.findall(r"id:\s+CUR-\d+", content))
    ix_c = len(re.findall(r"id:\s+PER-\d+", content))
    return RecordCompleteness(
        ix_a=ix_a, ix_b=ix_b, ix_c=ix_c, total_ix=ix_a + ix_b + ix_c
    )


def compute_intent_drift(window_days: int = 30) -> IntentDrift:
    events_path = PROFILE_DIR / "PIPELINE-EVENTS.jsonl"
    if not events_path.exists():
        return IntentDrift(0, {}, {}, {})
    now = datetime.now().timestamp()
    cutoff = now - max(1, window_days) * 86400
    by_source: dict[str, int] = {}
    by_rule: dict[str, int] = {}
    reject_cats: dict[str, int] = {}
    total = 0
    for line in events_path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError:
            continue
        if not isinstance(row, dict):
            continue
        ts_raw = str(row.get("ts") or "").strip()
        if ts_raw:
            try:
                ts = datetime.fromisoformat(ts_raw.replace("Z", "+00:00")).timestamp()
                if ts < cutoff:
                    continue
            except (ValueError, TypeError):
                pass
        event = str(row.get("event") or "")
        if event == "intent_conflict_cross_agent":
            total += 1
            source = str(row.get("candidate_source") or "unknown")
            rule_id = str(row.get("rule_id") or "UNKNOWN")
            by_source[source] = by_source.get(source, 0) + 1
            by_rule[rule_id] = by_rule.get(rule_id, 0) + 1
        elif event == "rejected":
            reason = str(row.get("rejection_reason") or "").lower()
            if "value_misalignment" in reason:
                key = "value_misalignment"
            elif "wrong_tradeoff" in reason:
                key = "wrong_tradeoff"
            elif reason:
                key = "other"
            else:
                continue
            reject_cats[key] = reject_cats.get(key, 0) + 1
    return IntentDrift(
        total_conflicts=total,
        conflicts_by_source=dict(sorted(by_source.items(), key=lambda kv: (-kv[1], kv[0]))),
        conflicts_by_rule=dict(sorted(by_rule.items(), key=lambda kv: (-kv[1], kv[0]))),
        rejection_categories=dict(sorted(reject_cats.items(), key=lambda kv: (-kv[1], kv[0]))),
    )


def report() -> str:
    """Human-readable metrics report."""
    health = compute_pipeline_health()
    completeness = compute_record_completeness()
    drift = compute_intent_drift()

    ar_str = f"{health.approval_rate:.1%}" if health.approval_rate is not None else "—"
    rr_str = f"{health.rejection_rate:.1%}" if health.rejection_rate is not None else "—"
    ds_str = f"{health.days_since_last_activity:.1f}" if health.days_since_last_activity is not None else "—"

    lines = [
        "# Grace-Mar Metrics",
        "",
        f"Generated: {datetime.now().isoformat()}",
        "",
        "## Pipeline Health",
        f"  Pending candidates: {health.pending_count}",
        f"  Stale (>7 days): {health.stale_candidates}",
        f"  Approval rate: {ar_str}",
        f"  Rejection rate: {rr_str}",
        f"  Applied total: {health.applied_total}",
        f"  Rejected total: {health.rejected_total}",
        f"  Last applied: {health.last_applied_ts or '—'}",
        f"  Days since activity: {ds_str}",
        "",
        "## Record Completeness",
        f"  IX-A (Knowledge): {completeness.ix_a}",
        f"  IX-B (Curiosity): {completeness.ix_b}",
        f"  IX-C (Personality): {completeness.ix_c}",
        f"  Total IX entries: {completeness.total_ix}",
        "",
        "## Intent Drift (30d)",
        f"  Cross-agent conflicts: {drift.total_conflicts}",
        f"  By source: {drift.conflicts_by_source or '—'}",
        f"  By rule: {drift.conflicts_by_rule or '—'}",
        f"  Rejection categories: {drift.rejection_categories or '—'}",
        "",
    ]

    if health.stale_candidates > 0:
        lines.append(f"⚠️  {health.stale_candidates} candidate(s) pending >7 days — consider review")
        lines.append("")
    if health.approval_rate is not None and health.approval_rate < 0.5:
        total = health.applied_total + health.rejected_total
        if total >= 10:
            lines.append("⚠️  Approval rate <50% — check for user fatigue or mismatch")
            lines.append("")

    return "\n".join(lines)


def main() -> None:
    import argparse
    parser = argparse.ArgumentParser(description="Pipeline health and record metrics")
    parser.add_argument("--json", action="store_true", help="Output JSON")
    parser.add_argument("--user", "-u", default="grace-mar", help="User id")
    args = parser.parse_args()

    global PROFILE_DIR
    PROFILE_DIR = REPO_ROOT / "users" / args.user

    health = compute_pipeline_health()
    completeness = compute_record_completeness()
    drift = compute_intent_drift()

    if args.json:
        out = {
            "pipeline_health": {
                "stale_candidates": health.stale_candidates,
                "pending_count": health.pending_count,
                "approval_rate": health.approval_rate,
                "rejection_rate": health.rejection_rate,
                "applied_total": health.applied_total,
                "rejected_total": health.rejected_total,
                "last_applied_ts": health.last_applied_ts,
                "days_since_last_activity": health.days_since_last_activity,
            },
            "record_completeness": {
                "ix_a": completeness.ix_a,
                "ix_b": completeness.ix_b,
                "ix_c": completeness.ix_c,
                "total_ix": completeness.total_ix,
            },
            "intent_drift": {
                "window_days": 30,
                "total_conflicts": drift.total_conflicts,
                "conflicts_by_source": drift.conflicts_by_source,
                "conflicts_by_rule": drift.conflicts_by_rule,
                "rejection_categories": drift.rejection_categories,
            },
        }
        print(json.dumps(out, indent=2))
    else:
        print(report())


if __name__ == "__main__":
    main()

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
PROFILE_DIR = REPO_ROOT / "users" / "pilot-001"
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


def report() -> str:
    """Human-readable metrics report."""
    health = compute_pipeline_health()
    completeness = compute_record_completeness()

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
    parser.add_argument("--user", "-u", default="pilot-001", help="User id")
    args = parser.parse_args()

    global PROFILE_DIR
    PROFILE_DIR = REPO_ROOT / "users" / args.user

    health = compute_pipeline_health()
    completeness = compute_record_completeness()

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
        }
        print(json.dumps(out, indent=2))
    else:
        print(report())


if __name__ == "__main__":
    main()

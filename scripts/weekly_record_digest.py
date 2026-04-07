#!/usr/bin/env python3
"""
Weekly Record digest — automated summary of Record growth over a window.

Combines git history, pipeline events, Evidence entry counts, and IX
section analysis into a growth report.

Usage:
    python scripts/weekly_record_digest.py -u grace-mar
    python scripts/weekly_record_digest.py -u grace-mar --days 14
    python scripts/weekly_record_digest.py -u grace-mar --json
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from collections import Counter
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

DEFAULT_USER = "grace-mar"
DEFAULT_DAYS = 7

RECORD_FILES = [
    "self.md",
    "self-archive.md",
    "self-evidence.md",
    "recursion-gate.md",
]


# ---------------------------------------------------------------------------
# Git history
# ---------------------------------------------------------------------------

def _git_log_record_commits(user_id: str, days: int) -> list[dict]:
    """Get commits touching Record files in the window."""
    since = (date.today() - timedelta(days=days)).isoformat()
    user_dir = f"users/{user_id}/"
    paths = [user_dir + f for f in RECORD_FILES] + ["bot/prompt.py"]

    try:
        r = subprocess.run(
            ["git", "log", f"--since={since}", "--pretty=format:%H|%ai|%s", "--"] + paths,
            capture_output=True, text=True, cwd=str(REPO_ROOT), timeout=10,
        )
        if r.returncode != 0:
            return []
    except Exception:
        return []

    commits = []
    for line in r.stdout.strip().splitlines():
        if not line.strip():
            continue
        parts = line.split("|", 2)
        if len(parts) == 3:
            commits.append({
                "hash": parts[0][:8],
                "date": parts[1][:10],
                "message": parts[2],
            })
    return commits


# ---------------------------------------------------------------------------
# Pipeline events
# ---------------------------------------------------------------------------

def _parse_pipeline_events(user_id: str, days: int) -> dict:
    """Count pipeline events by type in the window."""
    events_path = REPO_ROOT / "users" / user_id / "pipeline-events.jsonl"
    if not events_path.is_file():
        return {"staged": 0, "applied": 0, "rejected": 0, "total": 0}

    cutoff = (date.today() - timedelta(days=days)).isoformat()
    counts: Counter = Counter()

    for line in events_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        ts = str(event.get("timestamp", event.get("ts", "")))[:10]
        if ts >= cutoff:
            action = event.get("event", event.get("action", "other"))
            counts[action] += 1

    return {
        "staged": counts.get("staged", 0),
        "applied": counts.get("applied", 0),
        "rejected": counts.get("rejected", 0),
        "total": sum(counts.values()),
    }


# ---------------------------------------------------------------------------
# Evidence entry counts
# ---------------------------------------------------------------------------

def _find_evidence_path(user_id: str) -> Path | None:
    user_dir = REPO_ROOT / "users" / user_id
    for name in ("self-archive.md", "self-evidence.md"):
        p = user_dir / name
        if p.is_file():
            return p
    return None


def _count_evidence_by_type(user_id: str) -> dict[str, int]:
    """Count all Evidence entries by type prefix."""
    evidence_path = _find_evidence_path(user_id)
    if not evidence_path:
        return {}
    content = evidence_path.read_text(encoding="utf-8")
    counts: Counter = Counter()
    for m in re.finditer(r"- id:\s*(ACT|READ|WRITE|CREATE|MEDIA|LEARN|CUR|PER)-\d+", content):
        counts[m.group(1)] += 1
    return dict(counts)


def _count_recent_evidence(user_id: str, days: int) -> dict[str, int]:
    """Count Evidence entries within the date window."""
    evidence_path = _find_evidence_path(user_id)
    if not evidence_path:
        return {}
    content = evidence_path.read_text(encoding="utf-8")
    cutoff = (date.today() - timedelta(days=days)).isoformat()
    counts: Counter = Counter()
    for m in re.finditer(
        r"- id:\s*((?:ACT|READ|WRITE|CREATE|MEDIA|LEARN|CUR|PER)-\d+)",
        content,
    ):
        entry_type = m.group(1).split("-")[0]
        date_match = re.search(r"date:\s*(\d{4}-\d{2}-\d{2})", content[m.end(): m.end() + 500])
        if date_match and date_match.group(1) >= cutoff:
            counts[entry_type] += 1
    return dict(counts)


# ---------------------------------------------------------------------------
# IX section counts
# ---------------------------------------------------------------------------

def _count_ix_entries(user_id: str) -> dict[str, int]:
    """Count entries in IX-A, IX-B, IX-C (or separate files)."""
    user_dir = REPO_ROOT / "users" / user_id
    counts: dict[str, int] = {"knowledge": 0, "curiosity": 0, "personality": 0}

    self_path = user_dir / "self.md"
    if self_path.is_file():
        content = self_path.read_text(encoding="utf-8")
        counts["knowledge"] = len(re.findall(r"(?:LEARN|KNOW)-\d+", content))
        counts["curiosity"] = len(re.findall(r"CUR-\d+", content))
        counts["personality"] = len(re.findall(r"PER-\d+", content))
        if any(v > 0 for v in counts.values()):
            return counts

    for filename, key in [
        ("self-knowledge.md", "knowledge"),
        ("self-curiosity.md", "curiosity"),
        ("self-personality.md", "personality"),
    ]:
        p = user_dir / filename
        if p.is_file():
            content = p.read_text(encoding="utf-8")
            counts[key] = len(re.findall(r"(?:LEARN|KNOW|CUR|PER)-\d+", content))

    return counts


# ---------------------------------------------------------------------------
# PRP freshness
# ---------------------------------------------------------------------------

def _prp_freshness(user_id: str) -> dict:
    """Check PRP file age relative to last Record change."""
    prp_pattern = REPO_ROOT / f"{user_id}-llm.txt"
    prp_files = list(REPO_ROOT.glob("*-llm.txt"))
    if not prp_files:
        return {"exists": False, "stale": None}

    prp_path = prp_files[0]
    try:
        prp_mtime = datetime.fromtimestamp(prp_path.stat().st_mtime)
        self_path = REPO_ROOT / "users" / user_id / "self.md"
        if self_path.is_file():
            self_mtime = datetime.fromtimestamp(self_path.stat().st_mtime)
            stale = prp_mtime < self_mtime
        else:
            stale = None
        return {
            "exists": True,
            "path": str(prp_path.name),
            "stale": stale,
            "prp_modified": prp_mtime.strftime("%Y-%m-%d"),
        }
    except Exception:
        return {"exists": True, "stale": None}


# ---------------------------------------------------------------------------
# Pending gate count
# ---------------------------------------------------------------------------

def _pending_gate_count(user_id: str) -> int:
    gate_path = REPO_ROOT / "users" / user_id / "recursion-gate.md"
    if not gate_path.is_file():
        return 0
    content = gate_path.read_text(encoding="utf-8")
    processed = re.search(r"^## Processed\s*$", content, re.MULTILINE)
    section = content[:processed.start()] if processed else content
    return len(re.findall(r"status:\s*pending", section))


# ---------------------------------------------------------------------------
# Digest assembly
# ---------------------------------------------------------------------------

def compute_digest(user_id: str, days: int = DEFAULT_DAYS) -> dict:
    """Compute the full weekly digest. Returns structured dict."""
    commits = _git_log_record_commits(user_id, days)
    pipeline = _parse_pipeline_events(user_id, days)
    recent_evidence = _count_recent_evidence(user_id, days)
    total_evidence = _count_evidence_by_type(user_id)
    ix_counts = _count_ix_entries(user_id)
    prp = _prp_freshness(user_id)
    pending = _pending_gate_count(user_id)

    gap_result = None
    try:
        from detect_capture_gap import detect_gap
        gap_result = detect_gap(user_id)
    except ImportError:
        try:
            from scripts.detect_capture_gap import detect_gap
            gap_result = detect_gap(user_id)
        except ImportError:
            pass

    return {
        "user_id": user_id,
        "window_days": days,
        "generated": date.today().isoformat(),
        "commits": {
            "count": len(commits),
            "recent": commits[:5],
        },
        "pipeline": pipeline,
        "evidence": {
            "new_in_window": recent_evidence,
            "total": total_evidence,
        },
        "ix": ix_counts,
        "prp": prp,
        "gate_pending": pending,
        "capture_gap": gap_result,
    }


def format_digest(d: dict) -> str:
    """Format digest as readable markdown."""
    lines = [
        f"# Record Digest — {d['user_id']} ({d['window_days']}d window)",
        f"Generated: {d['generated']}",
        "",
    ]

    pl = d["pipeline"]
    lines.append("## Pipeline")
    lines.append(
        f"- Staged: {pl['staged']} | Applied: {pl['applied']} | Rejected: {pl['rejected']}"
    )
    lines.append(f"- Gate pending: {d['gate_pending']}")
    lines.append("")

    lines.append("## Evidence Growth")
    new_ev = d["evidence"]["new_in_window"]
    if new_ev:
        parts = [f"{t}: +{c}" for t, c in sorted(new_ev.items())]
        lines.append(f"- New in window: {', '.join(parts)}")
    else:
        lines.append("- New in window: none")
    total_ev = d["evidence"]["total"]
    if total_ev:
        parts = [f"{t}: {c}" for t, c in sorted(total_ev.items())]
        lines.append(f"- Total: {', '.join(parts)}")
    lines.append("")

    ix = d["ix"]
    lines.append("## Mind Growth (IX)")
    lines.append(
        f"- Knowledge: {ix.get('knowledge', 0)} | "
        f"Curiosity: {ix.get('curiosity', 0)} | "
        f"Personality: {ix.get('personality', 0)}"
    )
    lines.append("")

    prp = d["prp"]
    lines.append("## PRP Status")
    if prp.get("exists"):
        stale_tag = "STALE" if prp.get("stale") else "current"
        lines.append(f"- {prp.get('path', '?')} — {stale_tag} (modified {prp.get('prp_modified', '?')})")
    else:
        lines.append("- No PRP file found")
    lines.append("")

    cg = d.get("capture_gap") or {}
    if cg:
        lines.append("## Capture Health")
        level = cg.get("level", "unknown")
        days_since = cg.get("days_since_evidence")
        eid = cg.get("last_evidence_id", "?")
        if days_since is not None:
            lines.append(f"- {level.upper()}: {days_since}d since {eid}")
        else:
            lines.append(f"- {level.upper()}")
        lines.append("")

    commits = d["commits"]
    if commits["count"] > 0:
        lines.append(f"## Record Commits ({commits['count']})")
        for c in commits["recent"]:
            lines.append(f"- `{c['hash']}` {c['date']} — {c['message'][:80]}")
        if commits["count"] > 5:
            lines.append(f"  … and {commits['count'] - 5} more")

    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(description="Weekly Record growth digest.")
    ap.add_argument(
        "-u", "--user",
        default=os.getenv("GRACE_MAR_USER_ID", DEFAULT_USER).strip() or DEFAULT_USER,
    )
    ap.add_argument("--days", type=int, default=DEFAULT_DAYS, help="Window in days (default: 7)")
    ap.add_argument("--json", action="store_true", help="Output JSON")
    args = ap.parse_args()

    digest = compute_digest(args.user, args.days)

    if args.json:
        print(json.dumps(digest, indent=2, default=str))
    else:
        print(format_digest(digest))

    return 0


if __name__ == "__main__":
    sys.exit(main())

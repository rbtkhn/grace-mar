#!/usr/bin/env python3
"""
Session observability — companion-self-native metrics in one pass.

Template-portable (companion-self + grace-mar).

Reports: seeds created/updated, promotions staged, contradictions,
approaching claims, gate candidates pending, authority level,
surfaces touched (exploratory vs durable).

Usage:
  python3 scripts/session_observability.py -u grace-mar
  python3 scripts/session_observability.py -u grace-mar --since "2h"
  python3 scripts/session_observability.py -u grace-mar --json
  python3 scripts/session_observability.py -u grace-mar --oneline
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_USER_ID = "grace-mar"

DURABLE_PATTERNS = [
    "users/*/self.md",
    "users/*/self-archive.md",
    "users/*/self-skills.md",
    "users/*/recursion-gate.md",
    "bot/prompt.py",
]

EXPLORATORY_PATTERNS = [
    "users/*/self-memory.md",
    "users/*/session-log.md",
    "users/*/session-transcript.md",
    "docs/skill-work/",
    ".cursor/",
]


def _parse_since(since: str) -> datetime:
    """Parse a relative time like '2h', '30m', '1d' into a datetime."""
    m = re.match(r"^(\d+)([hmds])$", since.strip())
    if not m:
        try:
            return datetime.fromisoformat(since)
        except ValueError:
            return datetime.now(timezone.utc) - timedelta(hours=2)
    val, unit = int(m.group(1)), m.group(2)
    delta = {"h": timedelta(hours=val), "m": timedelta(minutes=val),
             "d": timedelta(days=val), "s": timedelta(seconds=val)}[unit]
    return datetime.now(timezone.utc) - delta


def _load_seed_registry(user_id: str) -> dict[str, list[dict[str, Any]]]:
    path = REPO_ROOT / "users" / user_id / "seed-registry.jsonl"
    if not path.exists():
        return {}
    history: dict[str, list[dict[str, Any]]] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            row = json.loads(line)
            sid = row.get("seed_id", "")
            if sid:
                history.setdefault(sid, []).append(row)
        except json.JSONDecodeError:
            continue
    return history


def _count_seed_activity(history: dict[str, list[dict[str, Any]]], since: datetime) -> dict[str, Any]:
    created = 0
    updated = 0
    promoted_to_candidate = 0
    contradictions_added = 0

    for sid, snaps in history.items():
        for i, snap in enumerate(snaps):
            try:
                ts = datetime.fromisoformat(snap.get("last_seen", ""))
            except (ValueError, TypeError):
                continue
            if ts.tzinfo is None:
                ts = ts.replace(tzinfo=timezone.utc)
            if ts < since:
                continue

            if i == 0:
                created += 1
            else:
                updated += 1

            if snap.get("status") == "candidate" and i > 0:
                prev = snaps[i - 1]
                if prev.get("status") != "candidate":
                    promoted_to_candidate += 1

            if i > 0:
                prev_ctrds = snaps[i - 1].get("contradiction_count", 0)
                cur_ctrds = snap.get("contradiction_count", 0)
                if cur_ctrds > prev_ctrds:
                    contradictions_added += cur_ctrds - prev_ctrds

    return {
        "seeds_created": created,
        "seeds_updated": updated,
        "promotions_staged": promoted_to_candidate,
        "contradictions_introduced": contradictions_added,
    }


def _count_approaching(user_id: str) -> int:
    try:
        sys.path.insert(0, str(REPO_ROOT / "scripts"))
        from evaluate_seed_promotion import evaluate_all, _load_rules
        rules = _load_rules()
        results = evaluate_all(user_id, rules)
        return sum(1 for r in results if r["verdict"] == "approaching")
    except Exception:
        return 0


def _count_gate_pending(user_id: str) -> int:
    gate_path = REPO_ROOT / "users" / user_id / "recursion-gate.md"
    if not gate_path.exists():
        gate_json = REPO_ROOT / "users" / user_id / "recursion-gate.json"
        if gate_json.exists():
            try:
                data = json.loads(gate_json.read_text(encoding="utf-8"))
                return sum(1 for c in data.get("candidates", [])
                           if c.get("status") == "pending")
            except (json.JSONDecodeError, KeyError):
                return 0
        return 0
    text = gate_path.read_text(encoding="utf-8")
    return len(re.findall(r"status:\s*pending", text))


def _load_authority_map() -> dict[str, str]:
    path = REPO_ROOT / "config" / "authority-map.json"
    if not path.exists():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        return data.get("surfaces", {})
    except (json.JSONDecodeError, KeyError):
        return {}


def _classify_surfaces(since: datetime) -> dict[str, list[str]]:
    """Classify recently changed files as durable or exploratory using git."""
    since_str = since.strftime("%Y-%m-%dT%H:%M:%S")
    try:
        result = subprocess.run(
            ["git", "diff", "--name-only", f"--since={since_str}", "HEAD"],
            capture_output=True, text=True, cwd=str(REPO_ROOT), timeout=10,
        )
        if result.returncode != 0:
            result = subprocess.run(
                ["git", "diff", "--name-only", "HEAD~5", "HEAD"],
                capture_output=True, text=True, cwd=str(REPO_ROOT), timeout=10,
            )
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return {"durable": [], "exploratory": [], "other": []}

    files = [f.strip() for f in result.stdout.splitlines() if f.strip()]

    durable: list[str] = []
    exploratory: list[str] = []
    other: list[str] = []

    for f in files:
        is_durable = any(
            re.match(p.replace("*", ".*"), f)
            for p in DURABLE_PATTERNS
        )
        is_exploratory = any(f.startswith(p.rstrip("*")) for p in EXPLORATORY_PATTERNS)

        if is_durable:
            durable.append(f)
        elif is_exploratory:
            exploratory.append(f)
        else:
            other.append(f)

    return {"durable": durable, "exploratory": exploratory, "other": other}


def gather_metrics(user_id: str, since: datetime) -> dict[str, Any]:
    """Gather all session observability metrics in one pass."""
    history = _load_seed_registry(user_id)
    seed_activity = _count_seed_activity(history, since)
    approaching = _count_approaching(user_id)
    gate_pending = _count_gate_pending(user_id)
    authority = _load_authority_map()
    surfaces = _classify_surfaces(since)

    human_only_count = sum(1 for v in authority.values() if v == "human_only")
    review_required_count = sum(1 for v in authority.values() if v == "review_required")

    return {
        **seed_activity,
        "claims_approaching_promotion": approaching,
        "gate_candidates_pending": gate_pending,
        "authority_summary": {
            "human_only": human_only_count,
            "review_required": review_required_count,
            "total_surfaces": len(authority),
        },
        "surfaces_touched": {
            "durable": len(surfaces["durable"]),
            "exploratory": len(surfaces["exploratory"]),
            "other": len(surfaces["other"]),
            "durable_files": surfaces["durable"],
            "exploratory_files": surfaces["exploratory"],
        },
    }


def format_oneline(metrics: dict[str, Any]) -> str:
    parts = []
    sc = metrics["seeds_created"]
    su = metrics["seeds_updated"]
    if sc or su:
        parts.append(f"seeds +{sc}/~{su}")
    ps = metrics["promotions_staged"]
    if ps:
        parts.append(f"promoted {ps}")
    ci = metrics["contradictions_introduced"]
    if ci:
        parts.append(f"contradictions +{ci}")
    cap = metrics["claims_approaching_promotion"]
    if cap:
        parts.append(f"approaching {cap}")
    gp = metrics["gate_candidates_pending"]
    parts.append(f"gate {gp} pending")
    st = metrics["surfaces_touched"]
    parts.append(f"surfaces {st['durable']}d/{st['exploratory']}e")
    return " | ".join(parts) if parts else "no activity"


def format_full(metrics: dict[str, Any], user_id: str) -> str:
    lines: list[str] = []
    lines.append(f"  Session Observability — {user_id}")
    lines.append("  " + "-" * 60)

    lines.append(f"  Seeds created:           {metrics['seeds_created']}")
    lines.append(f"  Seeds updated:           {metrics['seeds_updated']}")
    lines.append(f"  Promotions staged:       {metrics['promotions_staged']}")
    lines.append(f"  Contradictions added:    {metrics['contradictions_introduced']}")
    lines.append(f"  Claims approaching:      {metrics['claims_approaching_promotion']}")
    lines.append(f"  Gate candidates pending: {metrics['gate_candidates_pending']}")

    auth = metrics["authority_summary"]
    lines.append(f"\n  Authority: {auth['human_only']} human-only, "
                 f"{auth['review_required']} review-required, "
                 f"{auth['total_surfaces']} total surfaces")

    st = metrics["surfaces_touched"]
    lines.append(f"\n  Surfaces touched: {st['durable']} durable, "
                 f"{st['exploratory']} exploratory, {st['other']} other")
    if st["durable_files"]:
        for f in st["durable_files"]:
            lines.append(f"    [durable] {f}")
    if st["exploratory_files"]:
        for f in st["exploratory_files"]:
            lines.append(f"    [exploratory] {f}")

    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Session observability metrics.")
    parser.add_argument("-u", "--user", default=DEFAULT_USER_ID)
    parser.add_argument("--since", default="2h",
                        help="Time window: '2h', '30m', '1d', or ISO datetime")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--oneline", action="store_true",
                        help="One-line summary for coffee/bridge embedding")
    args = parser.parse_args()

    since = _parse_since(args.since)
    metrics = gather_metrics(args.user, since)

    if args.json:
        print(json.dumps(metrics, indent=2))
    elif args.oneline:
        print(format_oneline(metrics))
    else:
        print(format_full(metrics, args.user))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""
Hint at possibly duplicate pending candidates in RECURSION-GATE.

Same profile_target + similar summary (word overlap) → likely merge one or reject.
Does not auto-edit; operator decides.

Usage:
    python scripts/pending_dedup_hint.py -u grace-mar
    python scripts/pending_dedup_hint.py -u grace-mar --min-similarity 0.4
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


def _read(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8")


def _words(s: str) -> set[str]:
    return {w.lower() for w in re.findall(r"[a-zA-Z][a-zA-Z0-9_-]{2,}", s)}


def _jaccard(a: set[str], b: set[str]) -> float:
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def _extract_pending(pr: str) -> list[dict]:
    out: list[dict] = []
    for m in re.finditer(r"### (CANDIDATE-\d+).*?```yaml\n(.*?)```", pr, re.DOTALL):
        block = m.group(2)
        if not re.search(r"status:\s*pending\b", block):
            continue
        sm = re.search(r"summary:\s*(.+?)(?:\n[a-z_]+:|\Z)", block, re.DOTALL)
        summary = (sm.group(1) if sm else "").strip()
        summary = re.sub(r"^\|\s*", "", summary).strip().strip("\"'")[:500]
        pt = re.search(r"profile_target:\s*(.+?)(?:\n|$)", block)
        target = (pt.group(1) if pt else "").strip()[:120]
        out.append({"id": m.group(1), "summary": summary, "profile_target": target, "words": _words(summary)})
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description="Pending candidate dedup hints (read-only)")
    ap.add_argument("-u", "--user", default="grace-mar")
    ap.add_argument(
        "--min-similarity",
        type=float,
        default=0.35,
        help="Min Jaccard(word) similarity to flag pair (default 0.35)",
    )
    args = ap.parse_args()
    pr_path = REPO_ROOT / "users" / args.user / "recursion-gate.md"
    pr = _read(pr_path)
    pending = _extract_pending(pr)
    if len(pending) < 2:
        print(f"Pending count: {len(pending)} — nothing to pair.")
        return 0

    by_id = {p["id"]: p for p in pending}
    min_sim = max(0.15, min(0.95, args.min_similarity))
    pairs: list[tuple[str, str, float, str]] = []
    for i, a in enumerate(pending):
        for b in pending[i + 1 :]:
            sim = _jaccard(a["words"], b["words"])
            same_lane = bool(a["profile_target"] and a["profile_target"] == b["profile_target"])
            flag = sim >= min_sim or (same_lane and sim >= 0.22 and len(a["words"]) >= 5 and len(b["words"]) >= 5)
            if not flag:
                continue
            reason = "similar summary" if sim >= min_sim else "same profile_target + word overlap"
            pairs.append((a["id"], b["id"], sim, reason))

    print(f"# Pending dedup hints ({args.user})")
    print(f"# min_similarity={min_sim:.2f}\n")
    if not pairs:
        print("No pairs flagged.")
        return 0
    seen: set[frozenset[str]] = set()
    for ida, idb, sim, reason in sorted(pairs, key=lambda x: -x[2]):
        key = frozenset((ida, idb))
        if key in seen:
            continue
        seen.add(key)
        sa = by_id[ida]["summary"][:120]
        sb = by_id[idb]["summary"][:120]
        print(f"- **{ida}** ↔ **{idb}** — Jaccard ~{sim:.2f} ({reason})")
        print(f"  - {ida}: {sa}{'…' if len(by_id[ida]['summary']) > 120 else ''}")
        print(f"  - {idb}: {sb}{'…' if len(by_id[idb]['summary']) > 120 else ''}")
        print()
    print("_Operator: merge one, reject duplicate, or keep both if intentionally distinct._")
    return 0


if __name__ == "__main__":
    sys.exit(main())

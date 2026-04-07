#!/usr/bin/env python3
"""
Suggest the single best next action from gate and seed state.

Template-portable (companion-self + grace-mar). Read-only — never writes files.

Usage:
  python3 scripts/suggest_best_move.py -u grace-mar
  python3 scripts/suggest_best_move.py -u grace-mar --json
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_USER_ID = "grace-mar"

STALE_THRESHOLD_DAYS = 14


def _load_gate_candidates(user_id: str) -> list[dict[str, Any]]:
    """Load parsed gate candidates if the review module is available."""
    try:
        sys.path.insert(0, str(REPO_ROOT / "scripts"))
        from recursion_gate_review import parse_review_candidates
        return parse_review_candidates(user_id)
    except Exception:
        return _load_gate_candidates_fallback(user_id)


def _load_gate_candidates_fallback(user_id: str) -> list[dict[str, Any]]:
    """Minimal gate parsing when the full review module isn't available."""
    import re
    gate_path = REPO_ROOT / "users" / user_id / "recursion-gate.md"
    if not gate_path.exists():
        gate_json = REPO_ROOT / "users" / user_id / "recursion-gate.json"
        if gate_json.exists():
            try:
                data = json.loads(gate_json.read_text(encoding="utf-8"))
                items = data if isinstance(data, list) else data.get("candidates", [])
                return [{"candidate_id": c.get("id", "?"), "status": c.get("status", "pending"),
                         "risk_tier": "review_batch", "age_days": 0, "title": c.get("summary", "")}
                        for c in items if isinstance(c, dict) and c.get("status", "pending") == "pending"]
            except (json.JSONDecodeError, KeyError):
                return []
        return []
    text = gate_path.read_text(encoding="utf-8")
    candidates = []
    for m in re.finditer(r"###\s+(CANDIDATE-\d+)\s*[(\[]?([^)\]\n]*)", text):
        cid = m.group(1)
        title = m.group(2).strip().rstrip(")")
        block_start = m.end()
        block_end = text.find("###", block_start)
        block = text[block_start:block_end] if block_end > 0 else text[block_start:]
        status_m = re.search(r"status:\s*(\w+)", block)
        status = status_m.group(1) if status_m else "pending"
        if status == "pending":
            candidates.append({
                "candidate_id": cid, "status": status, "title": title,
                "risk_tier": "review_batch", "age_days": 0,
            })
    return candidates


def _load_approaching_seeds(user_id: str) -> list[dict[str, Any]]:
    """Load seed claims with verdict=approaching."""
    try:
        sys.path.insert(0, str(REPO_ROOT / "scripts"))
        from evaluate_seed_promotion import evaluate_all, _load_rules
        rules = _load_rules()
        results = evaluate_all(user_id, rules)
        return [r for r in results if r["verdict"] == "approaching"]
    except Exception:
        return []


def suggest_best_move(user_id: str = DEFAULT_USER_ID) -> dict[str, Any]:
    """Compute the single best next action. Returns dict with move, source, rationale."""
    candidates = _load_gate_candidates(user_id)
    pending = [c for c in candidates if c.get("status") == "pending"]

    quick_merge = [c for c in pending
                   if c.get("risk_tier") == "quick_merge_eligible" and c.get("age_days", 0) <= STALE_THRESHOLD_DAYS]
    if quick_merge:
        best = min(quick_merge, key=lambda c: c.get("age_days", 0))
        cid = best.get("candidate_id", "?")
        title = best.get("title", "")
        label = f" ({title})" if title else ""
        return {
            "move": f"Approve {cid}{label}",
            "source": "gate",
            "rationale": "Quick-merge eligible, no conflicts",
        }

    approaching = _load_approaching_seeds(user_id)
    if approaching:
        best = approaching[0]
        sid = best.get("seed_id", "?")
        claim = best.get("claim_text", "")[:50]
        return {
            "move": f"Re-observe {sid} — \"{claim}\"",
            "source": "seed_registry",
            "rationale": "One step from candidate status",
        }

    stale = [c for c in pending if c.get("age_days", 0) > STALE_THRESHOLD_DAYS]
    if stale:
        oldest = max(stale, key=lambda c: c.get("age_days", 0))
        cid = oldest.get("candidate_id", "?")
        days = oldest.get("age_days", 0)
        return {
            "move": f"Review or reject {cid} (stale, {days} days)",
            "source": "gate",
            "rationale": f"Pending over {STALE_THRESHOLD_DAYS} days without action",
        }

    if pending:
        return {
            "move": f"Review {len(pending)} pending gate candidate(s)",
            "source": "gate",
            "rationale": "Pending candidates awaiting review",
        }

    return {
        "move": "No urgent actions. Pick highest-value lane work.",
        "source": "none",
        "rationale": "Gate clear, no approaching seeds",
    }


def format_oneline(result: dict[str, Any]) -> str:
    return result["move"]


def main() -> int:
    parser = argparse.ArgumentParser(description="Suggest the best next action.")
    parser.add_argument("-u", "--user", default=DEFAULT_USER_ID)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    result = suggest_best_move(args.user)

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(result["move"])

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

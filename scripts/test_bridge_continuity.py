#!/usr/bin/env python3
"""
Bridge Continuity Fidelity Harness — tests whether bridge + coffee
achieves lossless restart by capturing pre-bridge state, generating a
synthetic bridge prompt, parsing it back, and scoring dimension overlap.

No LLM calls. No API keys. Pure file I/O + regex. CI tier 1 compatible.

Usage:
    python scripts/test_bridge_continuity.py
    python scripts/test_bridge_continuity.py -u grace-mar -o results.json
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_USER = os.getenv("GRACE_MAR_USER_ID", "grace-mar")

TERRITORY_GLOB = "docs/skill-work/work-*/work-*-history.md"
RECENCY_DAYS = 7


# ── Snapshot capture ────────────────────────────────────────────────

def _read_optional(path: Path) -> str:
    if path.is_file():
        return path.read_text(encoding="utf-8")
    return ""


def _pending_candidates(gate_text: str) -> list[str]:
    """Extract CANDIDATE-XXXX ids with status: pending from the gate file."""
    ids: list[str] = []
    current_id: str | None = None
    in_processed = False
    for line in gate_text.splitlines():
        if line.strip().startswith("## Processed"):
            in_processed = True
        if in_processed:
            continue
        m = re.match(r"###\s+(CANDIDATE-\d+)", line)
        if m:
            current_id = m.group(1)
        if current_id and re.search(r"status:\s*pending", line):
            ids.append(current_id)
            current_id = None
    return ids


def _dream_handoff(dream_json_path: Path) -> dict[str, Any]:
    if not dream_json_path.is_file():
        return {"present": False}
    try:
        data = json.loads(dream_json_path.read_text(encoding="utf-8"))
        return {
            "present": True,
            "integrity_ok": data.get("integrity_ok"),
            "governance_ok": data.get("governance_ok"),
            "contradiction_count": data.get("contradiction_count", 0),
            "followups": data.get("followups", []),
        }
    except (json.JSONDecodeError, KeyError):
        return {"present": False}


def _recent_territories(repo_root: Path, days: int = RECENCY_DAYS) -> list[str]:
    """Return territory names with history entries in the last N days."""
    cutoff = datetime.now(timezone.utc) - timedelta(days=days)
    cutoff_str = cutoff.strftime("%Y-%m-%d")
    active: list[str] = []
    for path in sorted(repo_root.glob(TERRITORY_GLOB)):
        territory = path.parent.name
        text = path.read_text(encoding="utf-8")
        for m in re.finditer(r"##\s+(\d{4}-\d{2}-\d{2})", text):
            if m.group(1) >= cutoff_str:
                active.append(territory)
                break
    return active


def _memory_long_term(mem_text: str) -> list[str]:
    """Extract bullet items from the Long-term section of self-memory."""
    items: list[str] = []
    in_long = False
    for line in mem_text.splitlines():
        if re.match(r"^##\s+Long-term", line):
            in_long = True
            continue
        if in_long and re.match(r"^##\s+", line):
            break
        if in_long and line.strip().startswith("- "):
            items.append(line.strip().lstrip("- ").strip())
    return items


def _git_log(repo_root: Path, count: int = 5) -> list[dict[str, str]]:
    """Return last N commits as [{sha, message}]."""
    try:
        result = subprocess.run(
            ["git", "log", f"--oneline", f"-{count}"],
            cwd=repo_root,
            capture_output=True,
            text=True,
            timeout=10,
        )
        commits = []
        for line in result.stdout.strip().splitlines():
            parts = line.split(" ", 1)
            if len(parts) == 2:
                commits.append({"sha": parts[0], "message": parts[1]})
        return commits
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return []


def capture_snapshot(repo_root: Path, user_id: str) -> dict[str, Any]:
    users_dir = repo_root / "users" / user_id
    gate_text = _read_optional(users_dir / "recursion-gate.md")
    mem_text = _read_optional(users_dir / "self-memory.md")

    return {
        "gate_pending": _pending_candidates(gate_text),
        "dream": _dream_handoff(users_dir / "last-dream.json"),
        "territories": _recent_territories(repo_root),
        "memory_pointers": _memory_long_term(mem_text),
        "commits": _git_log(repo_root),
    }


# ── Synthetic bridge prompt ─────────────────────────────────────────

def generate_synthetic_bridge(snapshot: dict[str, Any]) -> str:
    """Build a bridge transfer prompt from a snapshot, matching the template format."""
    gate = snapshot["gate_pending"]
    dream = snapshot["dream"]
    territories = snapshot["territories"]
    commits = snapshot["commits"]
    memory = snapshot["memory_pointers"]

    date_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    gate_section = f"{len(gate)} pending."
    if gate:
        for cid in gate[:3]:
            gate_section += f"\n- {cid}"
    else:
        gate_section = "Gate clear."

    dream_section = "No dream handoff found."
    if dream.get("present"):
        dream_section = (
            f"integrity={'pass' if dream['integrity_ok'] else 'fail'}, "
            f"governance={'pass' if dream['governance_ok'] else 'fail'}, "
            f"contradictions={dream['contradiction_count']}"
        )
        if dream.get("followups"):
            dream_section += "\nFollowups: " + "; ".join(dream["followups"])

    territory_section = "\n".join(f"- {t}" for t in territories) if territories else "No recent territory motion."

    commit_section = "\n".join(f"{c['sha']} {c['message']}" for c in commits) if commits else "No commits."

    priority_section = "1. Continue current work — synthetic harness default"
    if territories:
        priority_section = "\n".join(
            f"{i+1}. {t} — recent motion in territory history"
            for i, t in enumerate(territories[:3])
        )
    if memory:
        priority_section += f"\n\nMemory pointer: {memory[0]}"

    return f"""# Session Bridge — {date_str}

## Arc
Synthetic bridge for continuity testing. Session state captured from on-disk surfaces.

## Carry-forward from last dream
{dream_section}

## RECURSION-GATE snapshot
{gate_section}

## Active territories
{territory_section}

## Priority lanes for next session
{priority_section}

## Watch this
**focus** — Continuity harness test — verify round-trip fidelity.

## Since last bridge
- First bridge state — no prior delta.

## Bridge transfer quality
- **Confidence:** high
- **Signals:** synthetic harness; gate readable; commits captured
- **Gaps:** narrative arc not machine-tested
- **Seal:** clean (synthetic)

## Next session posture
**Posture:** reorient — harness validation run

## Commits sealed in this bridge
Synthetic (no commits made). Residue commit: none / Substantive commit: none

## Recent commits
{commit_section}

## Agent surface
- **Cursor model:** synthetic-harness

## Instructions for next session
Paste as first message; assistant runs coffee Step 1. Parallel import: use harvest separately.

coffee
"""


# ── Parse-back ──────────────────────────────────────────────────────

def parse_bridge_prompt(prompt: str) -> dict[str, Any]:
    """Extract structured data back from a bridge transfer prompt."""
    parsed: dict[str, Any] = {}

    gate_match = re.search(r"## RECURSION-GATE snapshot\n(.+?)(?=\n## )", prompt, re.DOTALL)
    if gate_match:
        gate_block = gate_match.group(1)
        parsed["gate_pending"] = re.findall(r"(CANDIDATE-\d+)", gate_block)
        count_match = re.search(r"(\d+)\s+pending", gate_block)
        parsed["gate_count"] = int(count_match.group(1)) if count_match else 0
    else:
        parsed["gate_pending"] = []
        parsed["gate_count"] = 0

    dream_match = re.search(r"## Carry-forward from last dream\n(.+?)(?=\n## )", prompt, re.DOTALL)
    if dream_match:
        dream_block = dream_match.group(1)
        parsed["dream_present"] = "no dream" not in dream_block.lower() and "not found" not in dream_block.lower()
        parsed["dream_integrity"] = "integrity=pass" in dream_block
        parsed["dream_governance"] = "governance=pass" in dream_block
        c_match = re.search(r"contradictions=(\d+)", dream_block)
        parsed["dream_contradictions"] = int(c_match.group(1)) if c_match else None
    else:
        parsed["dream_present"] = False
        parsed["dream_integrity"] = None
        parsed["dream_governance"] = None
        parsed["dream_contradictions"] = None

    terr_match = re.search(r"## Active territories\n(.+?)(?=\n## )", prompt, re.DOTALL)
    if terr_match:
        terr_block = terr_match.group(1)
        parsed["territories"] = re.findall(r"work-[\w-]+", terr_block)
    else:
        parsed["territories"] = []

    commit_match = re.search(r"## Recent commits\n(.+?)(?=\n## )", prompt, re.DOTALL)
    if commit_match:
        commit_block = commit_match.group(1)
        parsed["commit_shas"] = re.findall(r"\b([0-9a-f]{7,12})\b", commit_block)
    else:
        parsed["commit_shas"] = []

    parsed["full_text"] = prompt
    return parsed


# ── Scoring ─────────────────────────────────────────────────────────

def score_dimension(name: str, snapshot: dict, parsed: dict) -> dict[str, Any]:
    """Score a single dimension. Returns {name, passed, score, detail}."""
    if name == "gate":
        expected = set(snapshot["gate_pending"])
        recovered = set(parsed.get("gate_pending", []))
        if not expected and not recovered:
            return {"name": name, "passed": True, "score": 1.0, "detail": "both empty"}
        if not expected:
            return {"name": name, "passed": len(recovered) == 0, "score": 1.0 if not recovered else 0.0,
                    "detail": f"expected empty, got {recovered}"}
        overlap = expected & recovered
        score = len(overlap) / len(expected) if expected else 1.0
        return {"name": name, "passed": score >= 1.0, "score": score,
                "detail": f"{len(overlap)}/{len(expected)} ids recovered"}

    if name == "dream":
        dream_snap = snapshot["dream"]
        if not dream_snap.get("present"):
            ok = not parsed.get("dream_present", False)
            return {"name": name, "passed": ok, "score": 1.0 if ok else 0.0,
                    "detail": "no dream in both" if ok else "phantom dream in parsed"}
        checks = 0
        matches = 0
        for field, parsed_key in [
            ("integrity_ok", "dream_integrity"),
            ("governance_ok", "dream_governance"),
        ]:
            checks += 1
            if dream_snap.get(field) == parsed.get(parsed_key):
                matches += 1
        checks += 1
        if dream_snap.get("contradiction_count") == parsed.get("dream_contradictions"):
            matches += 1
        score = matches / checks if checks else 1.0
        return {"name": name, "passed": score >= 1.0, "score": score,
                "detail": f"{matches}/{checks} dream fields match"}

    if name == "territories":
        expected = set(snapshot["territories"])
        recovered = set(parsed.get("territories", []))
        if not expected and not recovered:
            return {"name": name, "passed": True, "score": 1.0, "detail": "no active territories"}
        if not expected:
            return {"name": name, "passed": True, "score": 1.0, "detail": "none expected"}
        recall = len(expected & recovered) / len(expected) if expected else 1.0
        return {"name": name, "passed": recall >= 1.0, "score": recall,
                "detail": f"{len(expected & recovered)}/{len(expected)} territories recalled"}

    if name == "commits":
        expected_shas = {c["sha"] for c in snapshot["commits"]}
        recovered_shas = set(parsed.get("commit_shas", []))
        if not expected_shas:
            return {"name": name, "passed": True, "score": 1.0, "detail": "no commits expected"}
        found = sum(1 for s in expected_shas if any(r.startswith(s) or s.startswith(r) for r in recovered_shas))
        score = found / len(expected_shas)
        return {"name": name, "passed": score >= 1.0, "score": score,
                "detail": f"{found}/{len(expected_shas)} commit SHAs found"}

    if name == "memory":
        pointers = snapshot["memory_pointers"]
        if not pointers:
            return {"name": name, "passed": True, "score": 1.0, "detail": "no long-term pointers"}
        full_text = parsed.get("full_text", "").lower()
        found = sum(1 for p in pointers if any(word in full_text for word in p.lower().split()[:3]))
        score = found / len(pointers) if pointers else 1.0
        return {"name": name, "passed": score > 0, "score": score,
                "detail": f"{found}/{len(pointers)} pointers referenced (soft match)"}

    return {"name": name, "passed": False, "score": 0.0, "detail": "unknown dimension"}


DIMENSIONS = ["gate", "dream", "territories", "commits", "memory"]


def run_harness(repo_root: Path, user_id: str) -> dict[str, Any]:
    """Full round-trip: snapshot → synthetic bridge → parse-back → score."""
    snapshot = capture_snapshot(repo_root, user_id)
    bridge_prompt = generate_synthetic_bridge(snapshot)
    parsed = parse_bridge_prompt(bridge_prompt)

    results = []
    for dim in DIMENSIONS:
        results.append(score_dimension(dim, snapshot, parsed))

    scores = [r["score"] for r in results]
    overall = sum(scores) / len(scores) if scores else 0.0

    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "user_id": user_id,
        "dimensions": results,
        "overall_score": round(overall, 3),
        "passed": overall >= 0.8,
        "snapshot_summary": {
            "gate_pending_count": len(snapshot["gate_pending"]),
            "dream_present": snapshot["dream"].get("present", False),
            "active_territories": len(snapshot["territories"]),
            "commit_count": len(snapshot["commits"]),
            "memory_pointers": len(snapshot["memory_pointers"]),
        },
    }


# ── CLI ─────────────────────────────────────────────────────────────

def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("-u", "--user", default=DEFAULT_USER, help="User id (default: grace-mar)")
    ap.add_argument("-o", "--output", default=None, help="Write JSON results to file")
    ap.add_argument("-v", "--verbose", action="store_true", help="Print per-dimension detail")
    args = ap.parse_args()

    result = run_harness(REPO_ROOT, args.user)

    print(f"Bridge Continuity Fidelity — {len(result['dimensions'])} dimensions")
    print("=" * 60)

    for dim in result["dimensions"]:
        status = "PASS" if dim["passed"] else "FAIL"
        print(f"  [{status}] {dim['name']:15s}  score={dim['score']:.2f}  {dim['detail']}")

    print("=" * 60)
    overall_status = "PASS" if result["passed"] else "FAIL"
    print(f"Overall: {result['overall_score']:.1%} [{overall_status}]")

    if args.output:
        out_path = Path(args.output)
        out_path.write_text(json.dumps(result, indent=2), encoding="utf-8")
        print(f"Results written to {out_path}")

    if args.verbose:
        print(f"\nSnapshot: {json.dumps(result['snapshot_summary'], indent=2)}")

    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())

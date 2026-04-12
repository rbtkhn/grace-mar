#!/usr/bin/env python3
"""
Compress one WORK lane into a small markdown (or JSON) artifact with recovery paths.

This is a Context Efficiency Layer (CEL) helper — not a second Record and not the
JSON paste caps in config/context_budgets/ (see docs/skill-work/active-lane-compression.md).

Usage:
  python3 scripts/compress_active_lane.py --lane work-strategy
  python3 scripts/compress_active_lane.py --lane work-strategy --json
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILL_WORK = REPO_ROOT / "docs" / "skill-work"
DEFAULT_USER = os.getenv("GRACE_MAR_USER_ID", "grace-mar").strip() or "grace-mar"


def _normalize_lane(name: str) -> str:
    n = name.strip().lower()
    if not n.startswith("work-"):
        n = f"work-{n}"
    return n


def _lane_dir(lane: str) -> Path:
    d = SKILL_WORK / lane
    if not d.is_dir():
        raise FileNotFoundError(f"Lane directory not found: {d}")
    return d


def _read(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8")


def _objective_from_readme(text: str) -> str:
    m = re.search(r"\*\*Objective:\*\*\s*([^\n]+)", text)
    if m:
        return m.group(1).strip()
    m = re.search(r"^#\s+[^\n]+\n\n\*\*Objective:\*\*\s*([^\n]+)", text, re.MULTILINE)
    if m:
        return m.group(1).strip()
    return "(see lane README)"


def _self_work_bullet(sw: str, lane: str) -> str:
    """Find a bullet in Objectives mentioning the lane."""
    if "## Objectives" not in sw:
        return ""
    block = sw.split("## Objectives", 1)[1]
    if "##" in block:
        block = block.split("##", 1)[0]
    key = lane.replace("work-", "")
    for line in block.splitlines():
        line_stripped = line.strip()
        if not line_stripped.startswith("-") and not line_stripped.startswith("*"):
            continue
        if lane in line or f"**{lane}" in line or key in line.lower():
            return re.sub(r"^[-*]\s*", "", line_stripped).strip()
    return ""


def _ledger_excerpt(ledger_path: Path) -> tuple[str, str]:
    """Return (focus_hint, risk_line) from WORK-LEDGER if present."""
    text = _read(ledger_path)
    if not text:
        return "", ""
    focus = ""
    m = re.search(
        r"(?:### Current focus|## II\. LANE-SPECIFIC|### Current priorities)[^\n]*\n+((?:[ \t]*[-*].+\n?)+)",
        text,
        re.IGNORECASE,
    )
    if m:
        lines = [ln.strip() for ln in m.group(1).splitlines() if ln.strip().startswith(("-", "*"))]
        if lines:
            focus = re.sub(r"^[-*]\s*", "", lines[0])[:500]
    risk = ""
    if "Known failure" in text or "failure mode" in text.lower():
        m2 = re.search(r"(?:Known failure modes?|### Known failure)[^\n]*\n+([^\n]+)", text, re.IGNORECASE)
        if m2:
            risk = m2.group(1).strip()[:400]
    return focus, risk


def build_active_lane_payload(lane: str, user_id: str, repo_root: Path) -> dict:
    lane_n = _normalize_lane(lane)
    lane_path = _lane_dir(lane_n)
    readme = _read(lane_path / "README.md")
    objective = _objective_from_readme(readme) if readme else "(no README)"

    user_dir = repo_root / "users" / user_id
    sw = _read(user_dir / "self-work.md")
    sw_line = _self_work_bullet(sw, lane_n)

    ledger_candidates = [
        lane_path / "WORK-LEDGER.md",
        lane_path / f"{lane_n.replace('-', '_')}-ledger.md".lower(),
    ]
    focus, risk = "", ""
    for lc in ledger_candidates:
        if lc.exists():
            focus, risk = _ledger_excerpt(lc)
            break

    readme_rel = f"docs/skill-work/{lane_n}/README.md"
    self_rel = f"users/{user_id}/self-work.md"
    sources = [readme_rel, self_rel]
    if (lane_path / "WORK-LEDGER.md").exists():
        sources.insert(1, f"docs/skill-work/{lane_n}/WORK-LEDGER.md")

    current_objective = sw_line or objective
    recommendation = (
        f"Use **{readme_rel}** as the lane entry; align cross-lane sequencing with **{self_rel}**."
    )
    next_action = f"Open `{readme_rel}` and confirm today’s wedge; update `{self_rel}` if priorities shift."
    top_risk = risk or "(scan WORK-LEDGER Known failure modes if present)"

    return {
        "lane": lane_n,
        "current_objective": current_objective,
        "current_recommendation": recommendation,
        "next_action": next_action,
        "top_risk": top_risk,
        "relevant_source_paths": sources,
        "lane_focus_excerpt": focus,
    }


def build_active_lane_markdown(payload: dict) -> str:
    lines = [
        f"# Active lane — {payload['lane']}",
        "",
        f"**Current objective:** {payload['current_objective']}",
        "",
        f"**Recommendation:** {payload['current_recommendation']}",
        "",
        f"**Next action:** {payload['next_action']}",
        "",
        f"**Top risk:** {payload['top_risk']}",
        "",
    ]
    if payload.get("lane_focus_excerpt"):
        lines.extend(["## Ledger focus (excerpt)", "", payload["lane_focus_excerpt"], ""])
    lines.extend(
        [
            "## Source paths",
            "",
        ]
    )
    for p in payload["relevant_source_paths"]:
        lines.append(f"- `{p}`")
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Emit compact active-lane context (CEL).")
    parser.add_argument("--lane", required=True, help="Lane id, e.g. work-strategy or strategy")
    parser.add_argument("--user", "-u", default=DEFAULT_USER, help="User id for self-work.md")
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=REPO_ROOT,
        help="Repository root",
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=None,
        help="Write markdown (or JSON with --json) to this path",
    )
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of markdown")
    parser.add_argument(
        "--print",
        action="store_true",
        dest="print_stdout",
        help="Also print body to stdout after writing",
    )
    args = parser.parse_args()

    try:
        payload = build_active_lane_payload(args.lane, args.user, args.repo_root)
    except FileNotFoundError as e:
        print(str(e), file=sys.stderr)
        return 1

    if args.json:
        body = json.dumps(payload, indent=2, ensure_ascii=False) + "\n"
    else:
        body = build_active_lane_markdown(payload)

    out_path = args.out
    if out_path is None:
        lane_safe = payload["lane"]
        default_dir = args.repo_root / "artifacts" / "context"
        default_dir.mkdir(parents=True, exist_ok=True)
        suffix = ".json" if args.json else ".md"
        out_path = default_dir / f"active-lane-{lane_safe}{suffix}"

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(body, encoding="utf-8")
    print(f"Wrote {out_path}", file=sys.stderr)
    if args.print_stdout:
        print(body, end="")

    return 0


if __name__ == "__main__":
    sys.exit(main())

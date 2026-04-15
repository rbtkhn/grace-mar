#!/usr/bin/env python3
"""
Stage CMC SCHOLAR insights as RECURSION-GATE candidates.

Scans SCHOLAR ledgers in the civilization_memory repo for recent updates,
extracts key patterns (continuity engines, doctrines, procedural lessons),
and stages them as pending candidates in recursion-gate.md.

All changes are additive. Contradictions are preserved. No epistemic
authority is claimed — CMC material is SELF-LIBRARY / CIV-MEM reference,
not identity.

Usage:
    python3 scripts/ingest_from_cmc.py -u grace-mar
    python3 scripts/ingest_from_cmc.py -u grace-mar --civilization rome
    python3 scripts/ingest_from_cmc.py -u grace-mar --dry-run
"""

from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_USER_ID = os.getenv("GRACE_MAR_USER_ID", "grace-mar").strip() or "grace-mar"


def _get_cmc_path() -> Path | None:
    path = os.getenv("CIVILIZATION_MEMORY_PATH", "").strip()
    if path:
        p = Path(path).resolve()
        if p.is_dir():
            return p
    candidates = (
        REPO_ROOT / "research" / "repos" / "civilization_memory",
        REPO_ROOT / "repos" / "civilization_memory",
        REPO_ROOT.parent / "civilization_memory",
    )
    for c in candidates:
        if c.resolve().is_dir():
            return c.resolve()
    return None


def _scholar_files(cmc_root: Path, civilization: str | None = None) -> list[Path]:
    """Find SCHOLAR markdown files in CMC content tree."""
    content_dir = cmc_root / "content"
    if not content_dir.is_dir():
        return []
    pattern = "**/*SCHOLAR*.md"
    if civilization:
        pattern = f"civilizations/{civilization}/**/*SCHOLAR*.md"
    return sorted(content_dir.glob(pattern))


def _recently_modified(path: Path, days: int = 30) -> bool:
    """Check if file was modified within N days (via git or mtime)."""
    try:
        result = subprocess.run(
            ["git", "log", "-1", "--format=%ct", "--", str(path)],
            cwd=str(path.parent),
            capture_output=True,
            text=True,
            timeout=5,
        )
        if result.returncode == 0 and result.stdout.strip():
            ts = int(result.stdout.strip())
            age = datetime.now(timezone.utc).timestamp() - ts
            return age < days * 86400
    except Exception:
        pass
    age = datetime.now(timezone.utc).timestamp() - path.stat().st_mtime
    return age < days * 86400


def _extract_insights(scholar_path: Path) -> list[dict]:
    """Extract key insight blocks from a SCHOLAR file."""
    text = scholar_path.read_text(encoding="utf-8")
    insights = []

    heading_pattern = re.compile(r"^##\s+(.+)$", re.MULTILINE)
    sections = heading_pattern.split(text)

    for i in range(1, len(sections), 2):
        heading = sections[i].strip()
        body = sections[i + 1].strip() if i + 1 < len(sections) else ""
        if not body or len(body) < 50:
            continue

        keywords = {"doctrine", "mechanism", "continuity", "lesson", "pattern",
                     "principle", "strategy", "governance", "institution", "crisis"}
        heading_lower = heading.lower()
        body_lower = body[:500].lower()
        relevance = sum(1 for k in keywords if k in heading_lower or k in body_lower)
        if relevance == 0:
            continue

        snippet = body[:600].strip()
        if len(body) > 600:
            snippet += "..."

        insights.append({
            "heading": heading,
            "snippet": snippet,
            "source_file": str(scholar_path),
            "relevance_score": relevance,
        })

    insights.sort(key=lambda x: -x["relevance_score"])
    return insights[:5]


def _next_candidate_id(gate_path: Path) -> str:
    """Find the next available CANDIDATE-NNNN id."""
    if not gate_path.exists():
        return "CANDIDATE-0200"
    text = gate_path.read_text(encoding="utf-8")
    ids = [int(m.group(1)) for m in re.finditer(r"CANDIDATE-(\d+)", text)]
    if not ids:
        return "CANDIDATE-0200"
    return f"CANDIDATE-{max(ids) + 1:04d}"


def _format_candidate(candidate_id: str, insight: dict, civilization: str | None) -> str:
    """Format a single gate candidate block."""
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    source_rel = insight["source_file"]
    civ_label = civilization or "general"

    return f"""### {candidate_id} (CMC SCHOLAR insight — {civ_label})

```yaml
status: pending
timestamp: {today}
channel_key: operator:cmc-ingest
source: "CMC SCHOLAR: {Path(source_rel).name}"
mind_category: knowledge
signal_type: civilizational_insight
priority_score: 3
summary: "{insight['heading']}"
profile_target: LIBRARY/CIV-MEM
proposal_class: CIV_MEM_ADD
suggested_entry: |
  {insight['snippet']}
prompt_section: none
prompt_addition: none
```
"""


def stage_insights(
    user_id: str,
    civilization: str | None = None,
    dry_run: bool = False,
    max_insights: int = 10,
    recent_days: int = 30,
) -> list[dict]:
    """Main pipeline: scan SCHOLAR → extract → stage to gate."""
    cmc_root = _get_cmc_path()
    if not cmc_root:
        print("error: CMC repo not found. Set CIVILIZATION_MEMORY_PATH or clone to research/repos/civilization_memory/", file=sys.stderr)
        return []

    gate_path = REPO_ROOT / "users" / user_id / "recursion-gate.md"
    scholar_files = _scholar_files(cmc_root, civilization)

    if not scholar_files:
        print(f"No SCHOLAR files found{' for ' + civilization if civilization else ''}.", file=sys.stderr)
        return []

    recent = [f for f in scholar_files if _recently_modified(f, days=recent_days)]
    if not recent:
        print(f"No recently modified SCHOLAR files (within {recent_days} days).", file=sys.stderr)
        print(f"Total SCHOLAR files found: {len(scholar_files)}", file=sys.stderr)
        return []

    all_insights = []
    for sf in recent:
        all_insights.extend(_extract_insights(sf))

    all_insights.sort(key=lambda x: -x["relevance_score"])
    all_insights = all_insights[:max_insights]

    if not all_insights:
        print("No relevant insights extracted from SCHOLAR files.", file=sys.stderr)
        return []

    staged = []
    current_id = _next_candidate_id(gate_path)
    id_num = int(re.search(r"\d+", current_id).group())

    for insight in all_insights:
        cid = f"CANDIDATE-{id_num:04d}"
        block = _format_candidate(cid, insight, civilization)

        if dry_run:
            print(f"[DRY RUN] Would stage {cid}: {insight['heading']}")
            print(block)
            print()
        else:
            with open(gate_path, "a", encoding="utf-8") as f:
                f.write("\n" + block)
            print(f"Staged {cid}: {insight['heading']}")

        staged.append({"id": cid, "heading": insight["heading"], "source": insight["source_file"]})
        id_num += 1

    if not dry_run and staged:
        print(f"\n{len(staged)} candidate(s) staged in {gate_path.relative_to(REPO_ROOT)}")
        print("Run gate review to inspect before approval.")

    return staged


def main() -> int:
    ap = argparse.ArgumentParser(description="Stage CMC SCHOLAR insights to RECURSION-GATE")
    ap.add_argument("-u", "--user", default=DEFAULT_USER_ID, help="User ID")
    ap.add_argument("--civilization", help="Filter by civilization (e.g. rome, china)")
    ap.add_argument("--dry-run", action="store_true", help="Preview without writing")
    ap.add_argument("--max", type=int, default=10, help="Max insights to stage")
    ap.add_argument("--days", type=int, default=30, help="Recent modification window (days)")
    args = ap.parse_args()

    staged = stage_insights(
        user_id=args.user,
        civilization=args.civilization,
        dry_run=args.dry_run,
        max_insights=args.max,
        recent_days=args.days,
    )
    return 0 if staged or args.dry_run else 1


if __name__ == "__main__":
    sys.exit(main())

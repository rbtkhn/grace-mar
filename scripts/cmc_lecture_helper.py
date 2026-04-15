#!/usr/bin/env python3
"""
CMC Lecture Mode helper — reflection prompt generation and gate staging.

Accepts Lecture Mode output (pasted text or file), generates a reflection
prompt surfacing key civilizational patterns, and optionally stages the
result as a SKILLS/THINK candidate in recursion-gate.md.

Usage:
    python3 scripts/cmc_lecture_helper.py -u grace-mar -f lecture-output.txt
    python3 scripts/cmc_lecture_helper.py -u grace-mar --stdin
    python3 scripts/cmc_lecture_helper.py -u grace-mar -f lecture-output.txt --dry-run
    python3 scripts/cmc_lecture_helper.py -u grace-mar -f lecture-output.txt --stage
"""

from __future__ import annotations

import argparse
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_USER_ID = os.getenv("GRACE_MAR_USER_ID", "grace-mar").strip() or "grace-mar"

REFLECTION_PROMPT_TEMPLATE = """## CMC Lecture Reflection

**Source:** {source}
**Date:** {date}
**Key civilization(s):** {civilizations}

### Extracted patterns

{patterns}

### Reflection questions

{questions}

### Connections to active strategy work

{connections}
"""

STRATEGY_KEYWORDS = {
    "continuity", "institution", "governance", "succession", "doctrine",
    "crisis", "reform", "collapse", "adaptation", "legitimacy",
    "bureaucracy", "elite", "military", "trade", "diplomacy",
    "religion", "law", "tax", "census", "infrastructure",
}


def _extract_patterns(text: str) -> list[str]:
    """Extract key civilizational patterns from lecture text."""
    patterns = []

    heading_re = re.compile(r"^#+\s+(.+)$", re.MULTILINE)
    for m in heading_re.finditer(text):
        heading = m.group(1).strip()
        if any(kw in heading.lower() for kw in STRATEGY_KEYWORDS):
            patterns.append(heading)

    bullet_re = re.compile(r"^[-*]\s+(.+)$", re.MULTILINE)
    for m in bullet_re.finditer(text):
        line = m.group(1).strip()
        if len(line) > 30 and any(kw in line.lower() for kw in STRATEGY_KEYWORDS):
            patterns.append(line[:200])

    return patterns[:10]


def _detect_civilizations(text: str) -> list[str]:
    """Detect civilization names mentioned in the text."""
    known = [
        "Rome", "Byzantine", "Ottoman", "China", "Persia", "Egypt",
        "India", "Japan", "Mongol", "Arab", "Islamic", "Greek",
        "Mesopotamia", "Inca", "Aztec", "Maya", "Korea", "Vietnam",
        "Russia", "Britain", "France", "Spain", "Portugal",
    ]
    found = []
    text_lower = text.lower()
    for civ in known:
        if civ.lower() in text_lower:
            found.append(civ)
    return found or ["general"]


def _generate_reflection_questions(patterns: list[str], civilizations: list[str]) -> list[str]:
    """Generate reflection questions from extracted patterns."""
    questions = []

    if patterns:
        questions.append(f"What mechanism made '{patterns[0]}' durable or fragile?")

    if len(patterns) >= 2:
        questions.append(
            f"How do '{patterns[0]}' and '{patterns[1]}' interact — reinforcing or competing?"
        )

    if len(civilizations) >= 2:
        questions.append(
            f"Does the pattern from {civilizations[0]} have a parallel in {civilizations[1]}? "
            "Where does the analogy break?"
        )

    questions.append("What modern institution or crisis does this pattern illuminate? What doesn't transfer?")
    questions.append("Is there a falsifier — a case where this pattern should have applied but didn't?")

    return questions[:5]


def _generate_connections(patterns: list[str]) -> str:
    """Suggest connections to active strategy work."""
    lines = [
        "- Check case-index.md for existing cases that share these mechanisms",
        "- If a pattern is novel, consider seeding a new case entry",
        "- Review strategy-notebook for active threads where these patterns apply",
    ]
    if any("crisis" in p.lower() or "collapse" in p.lower() for p in patterns):
        lines.append("- Crisis/collapse patterns may connect to current-events watch items")
    if any("governance" in p.lower() or "institution" in p.lower() for p in patterns):
        lines.append("- Governance/institutional patterns may support decision-point analysis")
    return "\n".join(lines)


def generate_reflection(text: str, source_name: str = "CMC Lecture") -> str:
    """Generate a structured reflection prompt from lecture text."""
    patterns = _extract_patterns(text)
    civilizations = _detect_civilizations(text)
    questions = _generate_reflection_questions(patterns, civilizations)

    return REFLECTION_PROMPT_TEMPLATE.format(
        source=source_name,
        date=datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        civilizations=", ".join(civilizations),
        patterns="\n".join(f"- {p}" for p in patterns) if patterns else "- (no key patterns extracted — review manually)",
        questions="\n".join(f"{i+1}. {q}" for i, q in enumerate(questions)),
        connections=_generate_connections(patterns),
    )


def _next_candidate_id(gate_path: Path) -> str:
    if not gate_path.exists():
        return "CANDIDATE-0200"
    text = gate_path.read_text(encoding="utf-8")
    ids = [int(m.group(1)) for m in re.finditer(r"CANDIDATE-(\d+)", text)]
    if not ids:
        return "CANDIDATE-0200"
    return f"CANDIDATE-{max(ids) + 1:04d}"


def stage_to_gate(user_id: str, reflection: str, source_name: str, dry_run: bool = False) -> str | None:
    """Stage the reflection as a SKILLS/THINK candidate."""
    gate_path = REPO_ROOT / "users" / user_id / "recursion-gate.md"
    cid = _next_candidate_id(gate_path)
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    snippet = reflection[:400].replace("\n", " ").strip()
    if len(reflection) > 400:
        snippet += "..."

    block = f"""### {cid} (CMC Lecture reflection — THINK)

```yaml
status: pending
timestamp: {today}
channel_key: operator:cmc-lecture
source: "{source_name}"
mind_category: knowledge
signal_type: civilizational_insight
priority_score: 3
summary: "Lecture reflection: {source_name}"
profile_target: SKILLS/THINK
proposal_class: CIV_MEM_ADD
suggested_entry: |
  {snippet}
prompt_section: none
prompt_addition: none
```
"""

    if dry_run:
        print(f"[DRY RUN] Would stage {cid}")
        print(block)
        return cid

    with open(gate_path, "a", encoding="utf-8") as f:
        f.write("\n" + block)
    print(f"Staged {cid} in {gate_path.relative_to(REPO_ROOT)}")
    return cid


def main() -> int:
    ap = argparse.ArgumentParser(description="CMC Lecture Mode helper")
    ap.add_argument("-u", "--user", default=DEFAULT_USER_ID, help="User ID")
    input_group = ap.add_mutually_exclusive_group(required=True)
    input_group.add_argument("-f", "--file", help="Path to lecture output file")
    input_group.add_argument("--stdin", action="store_true", help="Read from stdin")
    ap.add_argument("--stage", action="store_true", help="Stage to recursion-gate")
    ap.add_argument("--dry-run", action="store_true", help="Preview without writing")
    ap.add_argument("--source", default="CMC Lecture", help="Source label")
    args = ap.parse_args()

    if args.stdin:
        text = sys.stdin.read()
    else:
        text = Path(args.file).read_text(encoding="utf-8")

    if not text.strip():
        print("error: empty input", file=sys.stderr)
        return 1

    reflection = generate_reflection(text, source_name=args.source)
    print(reflection)

    if args.stage or args.dry_run:
        cid = stage_to_gate(args.user, reflection, args.source, dry_run=args.dry_run)
        if cid:
            print(f"\nCandidate: {cid}")

    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""
Parse transcript for "We did [X]." lines and stage as candidates to recursion-gate.

Reduces friction in the formative loop: paste LLM session output, run this script,
candidates are appended to recursion-gate for operator review.

Usage:
    python scripts/parse_we_did.py -u grace-mar -i transcript.txt
    python scripts/parse_we_did.py -u grace-mar  # read from stdin
    echo 'We did [reading inference: Nutcracker].' | python scripts/parse_we_did.py -u grace-mar --dry-run
"""

import argparse
import os
import re
import sys
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
USER_ID = os.getenv("GRACE_MAR_USER_ID", "grace-mar").strip() or "grace-mar"
RECURSION_GATE_PATH = REPO_ROOT / "users" / USER_ID / "recursion-gate.md"

WE_DID_PATTERN = re.compile(r'[Ww]e\s+did\s+\[([^\]]+)\]\.?', re.IGNORECASE)


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def _write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def _next_candidate_id(content: str) -> str:
    ids = [int(m.group(1)) for m in re.finditer(r"CANDIDATE-(\d+)", content)]
    n = max(ids, default=0) + 1
    return f"CANDIDATE-{n:04d}"


def extract_we_did_lines(text: str) -> list[str]:
    """Extract all 'We did [X].' lines from text."""
    return [m.group(1).strip() for m in WE_DID_PATTERN.finditer(text)]


def stage_we_did_to_recursion_gate(
    user_id: str,
    transcript_path: Path | None,
    transcript_text: str | None,
    dry_run: bool = False,
) -> list[dict]:
    """
    Parse transcript for "We did [X]." lines, create candidates, append to recursion-gate.
    Returns list of dicts with {id, x, summary} for each staged candidate.
    """
    if transcript_text is not None:
        text = transcript_text
    elif transcript_path and transcript_path.exists():
        text = _read(transcript_path)
    else:
        return []

    items = extract_we_did_lines(text)
    if not items:
        return []

    gate_path = REPO_ROOT / "users" / user_id / "recursion-gate.md"
    content = _read(gate_path)
    if not content:
        return []

    staged = []
    running_content = content
    for x in items:
        cid = _next_candidate_id(running_content)
        # Truncate X for summary if long
        summary = x if len(x) <= 80 else x[:77] + "..."
        block = f"""
### {cid} (Lesson — We did [X])

```yaml
status: pending
timestamp: {datetime.now().strftime("%Y-%m-%d")}
channel_key: lesson_prompt
source: lesson transcript (We did [X] parser)
source_exchange:
  user: "We did [{x}]."
mind_category: knowledge
signal_type: we_did / lesson
priority_score: 3
summary: {summary}
profile_target: IX-A. KNOWLEDGE (or skill-think / EVIDENCE)
suggested_entry: Lesson activity completed — {x}. Log for formative loop; merge into skill-think or EVIDENCE if evidence-linked.
prompt_section: ""
prompt_addition: none
```
"""
        staged.append({"id": cid, "x": x, "summary": summary, "block": block})
        running_content = running_content + block

    # Insert new candidates before ## Processed (so they stay in Candidates section)
    if not dry_run and staged:
        blocks_text = "".join(s["block"] for s in staged)
        insert_marker = "\n## Processed\n"
        if insert_marker in content:
            content = content.replace(insert_marker, blocks_text + insert_marker, 1)
        else:
            content = content.rstrip() + "\n" + blocks_text
        _write(gate_path, content)

    return staged


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Parse transcript for 'We did [X].' lines and stage to recursion-gate"
    )
    parser.add_argument("--user", "-u", default=USER_ID, help="User id")
    parser.add_argument("--input", "-i", default=None, help="Input transcript file (default: stdin)")
    parser.add_argument("--dry-run", action="store_true", help="Print what would be staged, do not write")
    args = parser.parse_args()

    transcript_text = None
    transcript_path = None
    if args.input:
        transcript_path = Path(args.input)
        if not transcript_path.is_absolute():
            transcript_path = REPO_ROOT / transcript_path
    else:
        transcript_text = sys.stdin.read()

    staged = stage_we_did_to_recursion_gate(
        user_id=args.user,
        transcript_path=transcript_path,
        transcript_text=transcript_text,
        dry_run=args.dry_run,
    )

    if not staged:
        print("No 'We did [X].' lines found.", file=sys.stderr)
        return

    for s in staged:
        print(f"Staged {s['id']}: We did [{s['x']}]", file=sys.stderr if not args.dry_run else sys.stdout)
    gate_path = REPO_ROOT / "users" / args.user / "recursion-gate.md"
    if args.dry_run:
        print("(dry run — no changes written)", file=sys.stderr)
    else:
        print(f"Appended {len(staged)} candidate(s) to {gate_path}", file=sys.stderr)


if __name__ == "__main__":
    main()

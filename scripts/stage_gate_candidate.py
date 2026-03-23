#!/usr/bin/env python3
"""
Insert a pending RECURSION-GATE candidate from stdin or a file.

Writes one `### CANDIDATE-XXXX` + ```yaml``` block **immediately before** `## Processed`.
Stages only; Record files are unchanged until companion approval and merge.

Examples:

  echo "Note from session" | python scripts/stage_gate_candidate.py -u grace-mar
  python scripts/stage_gate_candidate.py -u grace-mar -f ./note.md --mind curiosity
  python scripts/stage_gate_candidate.py -u grace-mar --dry-run --summary "Test" <<< "body"

Work-politics territory (optional):

  python scripts/stage_gate_candidate.py -u grace-mar --territory work-politics <<< "milestone text"
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
SCORE_SCRIPT = REPO_ROOT / "scripts" / "score_gate_candidates.py"
_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from repo_io import profile_dir, read_path

try:
    from recursion_gate_territory import TERRITORY_WAP
except ImportError:
    from scripts.recursion_gate_territory import TERRITORY_WAP

DEFAULT_USER = "grace-mar"


def _candidate_ids(content: str) -> list[int]:
    nums: list[int] = []
    for m in re.finditer(r"\bCANDIDATE-(\d+)\b", content):
        nums.append(int(m.group(1)))
    return nums


def next_candidate_id(content: str) -> str:
    nums = _candidate_ids(content)
    n = max(nums) + 1 if nums else 1
    return f"CANDIDATE-{n:04d}"


def _yaml_double_quoted(s: str) -> str:
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'


def _literal_block(s: str, base_indent: str = "    ") -> str:
    """YAML literal block content for `key: |` (lines indented under operator)."""
    if not s.strip():
        return base_indent + "(empty)\n"
    lines = []
    for line in s.splitlines():
        lines.append(base_indent + line)
    return "\n".join(lines) + "\n"


def _slug_title(text: str, max_len: int = 56) -> str:
    one = " ".join(text.splitlines()[:1]).strip() or "staged paste"
    one = re.sub(r"\s+", " ", one)
    if len(one) > max_len:
        one = one[: max_len - 1].rstrip() + "…"
    return one


def build_block(
    *,
    candidate_id: str,
    title: str,
    summary: str,
    body: str,
    mind_category: str,
    channel_key: str,
    territory: str | None,
    timestamp: str,
    proposal_class: str | None = None,
) -> str:
    summary_one = summary.strip().replace("\n", " ")[:500]
    if len(summary_one) > 200:
        summary_one = summary_one[:197] + "..."

    op_literal = _literal_block(body.rstrip("\n"))

    lines = [
        f"### {candidate_id} ({title})",
        "",
        "```yaml",
        "status: pending",
        f"timestamp: {timestamp}",
        f"channel_key: {channel_key}",
    ]
    if territory:
        lines.append(f"territory: {territory}")
    if proposal_class:
        lines.append(f"proposal_class: {proposal_class}")
    lines.extend(
        [
            "source: operator — scripts/stage_gate_candidate.py",
            "source_exchange:",
            "  operator: |",
        ]
    )
    lines.append(op_literal.rstrip("\n"))
    lines.extend(
        [
            f"mind_category: {mind_category}",
            "signal_type: operator_paste",
            "priority_score: 3",
            f"summary: {_yaml_double_quoted(summary_one)}",
            "profile_target: IX-A. KNOWLEDGE",
            "suggested_entry: \"See source_exchange.operator (staged paste).\"",
            "prompt_section: YOUR KNOWLEDGE",
            "prompt_addition: none",
            "```",
            "",
        ]
    )
    return "\n".join(lines)


def insert_before_processed(full_md: str, block: str) -> str:
    m = re.search(r"^## Processed\s*$", full_md, re.MULTILINE)
    if not m:
        raise ValueError("recursion-gate.md must contain a ## Processed heading")
    return full_md[: m.start()] + block + full_md[m.start() :]


def main() -> int:
    ap = argparse.ArgumentParser(description="Stage a pending candidate from paste/file into recursion-gate.md")
    ap.add_argument("-u", "--user", default=os.getenv("GRACE_MAR_USER_ID", DEFAULT_USER).strip() or DEFAULT_USER)
    ap.add_argument("-f", "--file", type=Path, default=None, help="Read body from file (default: stdin)")
    ap.add_argument("--summary", default=None, help="One-line summary (default: first line of body)")
    ap.add_argument("--title", default=None, help="Short title for header (default: derived from summary)")
    ap.add_argument(
        "--mind",
        choices=("knowledge", "curiosity", "personality"),
        default="knowledge",
        help="mind_category (default: knowledge)",
    )
    ap.add_argument(
        "--territory",
        choices=("companion", "work-politics"),
        default="companion",
        help="companion = default Record channel; work-politics = territory + wap channel_key prefix",
    )
    ap.add_argument(
        "--channel-key",
        default=None,
        help="Override channel_key (default: operator:cursor:stage-paste or operator:wap:stage-paste)",
    )
    ap.add_argument("--dry-run", action="store_true", help="Print block to stdout; do not write")
    ap.add_argument(
        "--proposal-class",
        default=None,
        help="Optional YAML proposal_class (e.g. SIMULATION_RESULT for fork simulations)",
    )
    ap.add_argument(
        "--auto-score",
        action="store_true",
        help="After writing, run score_gate_candidates.py for this user (heuristic hints)",
    )
    args = ap.parse_args()

    if args.file:
        body = args.file.read_text(encoding="utf-8")
    else:
        body = sys.stdin.read()

    summary = args.summary
    if not summary:
        for line in body.splitlines():
            if line.strip():
                summary = line.strip()
                break
        else:
            summary = "(staged paste — empty body)"

    title = args.title or _slug_title(summary)

    if args.territory == "work-politics":
        territory = TERRITORY_WAP
        channel_key = args.channel_key or "operator:wap:stage-paste"
    else:
        territory = None
        channel_key = args.channel_key or "operator:cursor:stage-paste"

    ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")

    gate_path = profile_dir(args.user) / "recursion-gate.md"
    if not gate_path.exists():
        print(f"Missing {gate_path}", file=sys.stderr)
        return 1

    full = read_path(gate_path)
    if "## Candidates" not in full or "## Processed" not in full:
        print(f"{gate_path}: need ## Candidates and ## Processed", file=sys.stderr)
        return 1

    cid = next_candidate_id(full)
    block = build_block(
        candidate_id=cid,
        title=title,
        summary=summary,
        body=body,
        mind_category=args.mind,
        channel_key=channel_key,
        territory=territory,
        timestamp=ts,
        proposal_class=args.proposal_class,
    )

    if args.dry_run:
        print(block)
        print(f"# Would insert {cid} before ## Processed", file=sys.stderr)
        return 0

    try:
        new_full = insert_before_processed(full, block)
    except ValueError as e:
        print(e, file=sys.stderr)
        return 1

    gate_path.write_text(new_full, encoding="utf-8")
    print(f"{gate_path}: inserted {cid}")
    if args.auto_score and SCORE_SCRIPT.is_file():
        subprocess.run(
            [sys.executable, str(SCORE_SCRIPT), "-u", args.user],
            check=False,
        )
    elif args.auto_score:
        print(f"Missing {SCORE_SCRIPT}, skipping --auto-score", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

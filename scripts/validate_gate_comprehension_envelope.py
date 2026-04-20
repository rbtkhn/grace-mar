#!/usr/bin/env python3
"""
Warn if a pending candidate has envelope_class: required but no Comprehension Envelope block.

Markdown-first: envelope lives below the ```yaml fence in the same ### CANDIDATE- section.
Does not validate prose quality. Does not invoke process_approved_candidates.py.

Default: print warnings to stderr, exit 0.
With --strict: exit 1 if any pending required candidate is missing a non-empty envelope.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

try:
    from gate_block_parser import pending_candidates_region
except ImportError:
    from scripts.gate_block_parser import pending_candidates_region

try:
    from repo_io import REPO_ROOT, profile_dir
except ImportError:
    from scripts.repo_io import REPO_ROOT, profile_dir


def _scalar(yaml_body: str, key: str) -> str:
    m = re.search(rf"^{re.escape(key)}:\s*(.+)$", yaml_body, re.MULTILINE)
    if not m:
        return ""
    return m.group(1).strip().strip("\"'")


def _iter_candidate_sections(pending_region: str) -> list[tuple[str, str]]:
    """Return (candidate_id, full_section_text) for each ### CANDIDATE- block."""
    parts = re.split(r"(?=^### CANDIDATE-\d+)", pending_region, flags=re.MULTILINE)
    out: list[tuple[str, str]] = []
    for part in parts:
        part = part.strip()
        if not part.startswith("### CANDIDATE-"):
            continue
        m = re.match(r"^### (CANDIDATE-\d+)", part)
        if m:
            out.append((m.group(1), part))
    return out


def _envelope_present_and_non_empty(section: str) -> bool:
    """True if ### Comprehension Envelope exists and has at least one filled bullet line."""
    m = re.search(
        r"^### Comprehension Envelope\s*\n((?:.*\n)*?)(?=^### |\Z)",
        section,
        re.MULTILINE,
    )
    if not m:
        return False
    body = m.group(1)
    for line in body.splitlines():
        s = line.strip()
        if s.startswith("-") and len(s) > 1:
            rest = s[1:].strip()
            if rest and not rest.startswith("…"):
                return True
    return False


def validate_gate(gate_path: Path) -> list[str]:
    """Return human-readable problem lines (empty if ok)."""
    if not gate_path.is_file():
        return [f"not found: {gate_path}"]
    text = gate_path.read_text(encoding="utf-8")
    region = pending_candidates_region(text)
    problems: list[str] = []
    for cid, section in _iter_candidate_sections(region):
        ym = re.search(r"```yaml\n(.*?)```", section, re.DOTALL)
        if not ym:
            continue
        yaml_body = ym.group(1)
        if not re.search(r"^status:\s*pending\s*$", yaml_body, re.MULTILINE):
            continue
        env = _scalar(yaml_body, "envelope_class").lower()
        if env != "required":
            continue
        if not _envelope_present_and_non_empty(section):
            problems.append(
                f"{cid}: envelope_class is required but Comprehension Envelope is missing "
                "or has no filled bullet lines under the same candidate section"
            )
    return problems


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "-u",
        "--user",
        default="grace-mar",
        help="User id under users/ (default: grace-mar)",
    )
    ap.add_argument(
        "--gate",
        type=Path,
        default=None,
        help="Explicit path to recursion-gate.md (overrides -u)",
    )
    ap.add_argument(
        "--strict",
        action="store_true",
        help="Exit 1 if any problem is reported",
    )
    args = ap.parse_args()
    if args.gate:
        gate_path = args.gate
    else:
        gate_path = profile_dir(args.user) / "recursion-gate.md"
        if not gate_path.is_file():
            gate_path = REPO_ROOT / "users" / args.user / "recursion-gate.md"

    problems = validate_gate(gate_path)
    for p in problems:
        print(p, file=sys.stderr)
    if problems and args.strict:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

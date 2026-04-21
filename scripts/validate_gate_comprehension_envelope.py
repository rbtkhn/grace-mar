#!/usr/bin/env python3
"""
Validate Comprehension Envelope + Reflection Gates (v1) for pending candidates.

Markdown-first: envelope lives below the ```yaml fence in the same ### CANDIDATE- section.
Does not judge prose quality. Does not invoke process_approved_candidates.py.

- envelope_class: required → non-empty Comprehension Envelope (strict-eligible)
- impact_tier high|boundary (Heavy Gate) → advisory warnings for class, envelope, bullets
- impact_tier medium (Light Gate) → optional advisory if envelope missing

Default: print warnings to stderr, exit 0.
With --strict: exit 1 if strict-eligible problems exist (envelope required but missing/empty).
Heavy/Light advisory lines do not affect exit code unless they duplicate a strict case.
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


def _envelope_body(section: str) -> str:
    m = re.search(
        r"^### Comprehension Envelope\s*\n((?:.*\n)*?)(?=^### |\Z)",
        section,
        re.MULTILINE,
    )
    return m.group(1) if m else ""


def _envelope_present_and_non_empty(section: str) -> bool:
    """True if ### Comprehension Envelope exists and has at least one filled bullet line."""
    body = _envelope_body(section)
    if not body.strip():
        return False
    for line in body.splitlines():
        s = line.strip()
        if s.startswith("-") and len(s) > 1:
            rest = s[1:].strip()
            if rest and not rest.startswith("…"):
                return True
    return False


def _bullet_value_after_label(envelope_body: str, label: str) -> str:
    """First bullet `- Label: value` where label matches (case-insensitive on label part)."""
    prefix = label.strip().lower()
    for line in envelope_body.splitlines():
        line = line.strip()
        if not line.startswith("-"):
            continue
        rest = line[1:].strip()
        if ":" not in rest:
            continue
        lab, val = rest.split(":", 1)
        if lab.strip().lower() == prefix:
            return val.strip()
    return ""


def validate_gate(gate_path: Path) -> tuple[list[str], list[str]]:
    """
    Return (strict_problems, advisory_warnings).
    strict_problems: envelope_class required but envelope missing/empty (same as legacy).
    """
    if not gate_path.is_file():
        return [f"not found: {gate_path}"], []
    text = gate_path.read_text(encoding="utf-8")
    region = pending_candidates_region(text)
    strict_problems: list[str] = []
    advisory: list[str] = []

    for cid, section in _iter_candidate_sections(region):
        ym = re.search(r"```yaml\n(.*?)```", section, re.DOTALL)
        if not ym:
            continue
        yaml_body = ym.group(1)
        if not re.search(r"^status:\s*pending\s*$", yaml_body, re.MULTILINE):
            continue

        env_class = _scalar(yaml_body, "envelope_class").lower()
        impact = _scalar(yaml_body, "impact_tier").lower()
        has_env = _envelope_present_and_non_empty(section)
        env_text = _envelope_body(section)

        # Legacy strict: envelope_class required → must have envelope
        if env_class == "required" and not has_env:
            strict_problems.append(
                f"{cid}: envelope_class is required but Comprehension Envelope is missing "
                "or has no filled bullet lines under the same candidate section"
            )

        # Heavy Gate (impact_tier high | boundary)
        if impact in ("high", "boundary"):
            if env_class != "required":
                advisory.append(
                    f"{cid}: Heavy Gate (impact_tier {impact}): envelope_class should be "
                    f"'required' (got {(env_class or 'unset')!r})"
                )
            if not has_env:
                if env_class == "required":
                    pass  # already in strict_problems
                else:
                    advisory.append(
                        f"{cid}: Heavy Gate (impact_tier {impact}): Comprehension Envelope "
                        "missing or empty — required for Heavy Gate"
                    )
            elif env_text:
                br = _bullet_value_after_label(env_text, "Blast radius")
                ho = _bullet_value_after_label(env_text, "Human override applied")
                if not br:
                    advisory.append(
                        f"{cid}: Heavy Gate: Comprehension Envelope should include a filled "
                        "'Blast radius' bullet"
                    )
                if not ho:
                    advisory.append(
                        f"{cid}: Heavy Gate: Comprehension Envelope should include a filled "
                        "'Human override applied' bullet"
                    )

        # Light Gate (medium): recommend envelope, never strict here
        if impact == "medium" and not has_env:
            advisory.append(
                f"{cid}: Light Gate (impact_tier medium): Comprehension Envelope recommended "
                "(advisory; no hard block in v1)"
            )

    return strict_problems, advisory


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
        help="Exit 1 if any strict problem (envelope_class required but envelope missing)",
    )
    args = ap.parse_args()
    if args.gate:
        gate_path = args.gate
    else:
        gate_path = profile_dir(args.user) / "recursion-gate.md"
        if not gate_path.is_file():
            gate_path = REPO_ROOT / "users" / args.user / "recursion-gate.md"

    strict_problems, advisory = validate_gate(gate_path)
    for p in strict_problems:
        print(p, file=sys.stderr)
    for a in advisory:
        print(a, file=sys.stderr)
    if strict_problems and args.strict:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""
Heuristic auto-score for RECURSION-GATE candidates (pending section only by default).

Inserts a blockquote line after each `### CANDIDATE-...` heading (before the ```yaml
fence) so review surfaces (gate-review-app, Telegram, raw markdown) show scores
without changing merge semantics. Re-running replaces the previous Auto-score line.

This is **operator tooling**, not merge logic. Scores are hints; the companion still
approves/rejects. Does **not** call ``measure_growth_and_density`` / ``measure_uniqueness``
today (those lack stable ``--json`` for subprocess use); weights can be wired later.

Usage:
  python scripts/score_gate_candidates.py -u grace-mar --dry-run
  python scripts/score_gate_candidates.py -u grace-mar --threshold 65
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

try:
    from recursion_gate_review import split_gate_sections
    from repo_io import fork_root
except ImportError:
    from scripts.recursion_gate_review import split_gate_sections
    from scripts.repo_io import fork_root

# Weights sum to 1.0 — tune in fork policy or env later if needed
SCORE_WEIGHTS = {
    "density_delta": 0.25,
    "uniqueness": 0.30,
    "evidence_grounding": 0.20,
    "ix_balance": 0.15,
    "readability": 0.10,
}

DEFAULT_THRESHOLD = 65.0

# One candidate block: heading, optional blank lines, optional prior score line, yaml fence
_CANDIDATE_BLOCK_RE = re.compile(
    r"(### CANDIDATE-\d+[^\n]*\n)\s*(?:> \*\*Auto-score\*\*[^\n]*\n\s*)?(```yaml\n.*?```)",
    re.DOTALL,
)


def _yaml_body_from_fence(fence: str) -> str:
    if fence.startswith("```yaml\n") and fence.endswith("```"):
        return fence[len("```yaml\n") : -len("```")]
    return fence


def _is_pending_status(yaml_body: str) -> bool:
    """True when status is absent or explicitly pending (merge-ready queue)."""
    m = re.search(r"^status:\s*(\S+)", yaml_body, re.MULTILINE | re.IGNORECASE)
    if not m:
        return True
    return m.group(1).strip().lower() == "pending"


def estimate_subscores(text: str) -> dict[str, float]:
    """Deterministic 0..1 subscores from candidate text (heading + yaml)."""
    t = text or ""
    lower = t.lower()

    word_count = len(t.split())
    scores: dict[str, float] = {}

    scores["density_delta"] = min(1.0, word_count / 400.0)

    uniqueness_keywords = (
        "novel",
        "contradiction",
        "gap",
        "new evidence",
        "re-evaluate",
        "diverge",
        "abstain",
        "boundary",
        "duplicate",
        "overlap",
    )
    kw_hits = sum(1 for kw in uniqueness_keywords if kw in lower)
    scores["uniqueness"] = min(1.0, kw_hits / 3.0 + 0.2)

    evidence_indicators = re.compile(
        r"(artifact|evidence_id|evidence|ref:|https?://|20\d{2}-\d{2}-\d{2}|self-evidence\.md|ACT-\d+)",
        re.IGNORECASE,
    )
    evidence_matches = len(evidence_indicators.findall(t))
    scores["evidence_grounding"] = min(1.0, evidence_matches / 2.0)

    ix_a = len(re.findall(r"IX-A|knowledge|mind_category:\s*knowledge", t, re.I))
    ix_b = len(re.findall(r"IX-B|curiosity|mind_category:\s*curiosity", t, re.I))
    ix_c = len(re.findall(r"IX-C|personality|mind_category:\s*personality", t, re.I))
    total_ix = ix_a + ix_b + ix_c + 1e-6
    balance_score = 1.0 - max(ix_a, ix_b, ix_c) / total_ix
    scores["ix_balance"] = max(0.0, min(1.0, balance_score))

    sentence_count = max(1, len(re.split(r"[.!?]+", t)))
    avg_words_per_sent = word_count / sentence_count
    scores["readability"] = max(0.0, 1.0 - min(1.0, avg_words_per_sent / 35.0))

    return scores


def compute_composite(sub: dict[str, float]) -> float:
    total = sum(SCORE_WEIGHTS[k] * sub.get(k, 0.5) for k in SCORE_WEIGHTS)
    return round(total * 100.0, 1)


def _format_score_line(composite: float, sub: dict[str, float], low: bool) -> str:
    parts = (
        f"density {sub['density_delta']:.2f}",
        f"uniq {sub['uniqueness']:.2f}",
        f"ev {sub['evidence_grounding']:.2f}",
        f"bal {sub['ix_balance']:.2f}",
        f"read {sub['readability']:.2f}",
    )
    line = f"> **Auto-score**: {composite:.1f}/100 ({' · '.join(parts)})"
    if low:
        line += " **[LOW CONFIDENCE]**"
    return line + "\n"


def annotate_active_section(
    active: str,
    *,
    threshold: float,
    pending_only: bool,
) -> tuple[str, int]:
    """Return (new_active, n_scored) where n_scored counts blocks that received a new score line."""

    scored = 0

    def repl(m: re.Match[str]) -> str:
        nonlocal scored
        heading = m.group(1)
        fence = m.group(2)
        yaml_body = _yaml_body_from_fence(fence)
        if pending_only and not _is_pending_status(yaml_body):
            return m.group(0)

        text_for_score = heading + yaml_body
        sub = estimate_subscores(text_for_score)
        composite = compute_composite(sub)
        low = composite < threshold
        score_line = _format_score_line(composite, sub, low)
        scored += 1
        return heading + score_line + fence

    new_active = _CANDIDATE_BLOCK_RE.sub(repl, active)
    return new_active, scored


def score_gate_file(
    user_id: str,
    *,
    threshold: float = DEFAULT_THRESHOLD,
    dry_run: bool = False,
    pending_only: bool = True,
) -> tuple[Path, int]:
    gate_path = fork_root(user_id) / "recursion-gate.md"
    if not gate_path.is_file():
        print(f"No recursion-gate.md at {gate_path}", file=sys.stderr)
        return gate_path, 0

    full = gate_path.read_text(encoding="utf-8")
    active, processed = split_gate_sections(full)
    marker = re.search(r"^## Processed\s*$", full, re.MULTILINE)
    if marker:
        tail = full[marker.start() :]
        new_active, n = annotate_active_section(active, threshold=threshold, pending_only=pending_only)
        new_full = new_active + tail
    else:
        new_active, n = annotate_active_section(full, threshold=threshold, pending_only=pending_only)
        new_full = new_active

    if dry_run:
        print(f"[dry-run] Would update {n} candidate block(s) in {gate_path}")
        print("--- preview (first 1200 chars of active section) ---")
        prev, _ = split_gate_sections(new_full)
        print(prev[:1200])
        if len(prev) > 1200:
            print("... [truncated]")
        return gate_path, n

    gate_path.write_text(new_full, encoding="utf-8")
    print(f"Updated {gate_path} — scored {n} candidate block(s) (threshold {threshold}).")
    return gate_path, n


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Insert heuristic Auto-score blockquotes into recursion-gate.md (active section)."
    )
    parser.add_argument("-u", "--user", default="grace-mar", help="Fork id under users/")
    parser.add_argument(
        "--threshold",
        type=float,
        default=DEFAULT_THRESHOLD,
        help=f"Mark scores below this as LOW CONFIDENCE (default {DEFAULT_THRESHOLD:g})",
    )
    parser.add_argument("--dry-run", action="store_true", help="Print preview; do not write")
    parser.add_argument(
        "--all-status",
        action="store_true",
        help="Score every candidate block, not only pending (includes rejected/approved in Candidates)",
    )
    args = parser.parse_args()

    _, n = score_gate_file(
        args.user,
        threshold=args.threshold,
        dry_run=args.dry_run,
        pending_only=not args.all_status,
    )
    return 0 if n >= 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())

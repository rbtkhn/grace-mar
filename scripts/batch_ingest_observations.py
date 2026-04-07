#!/usr/bin/env python3
"""
Batch observation ingest — stage multiple RECURSION-GATE candidates from
a simple text file (or stdin) in one pass.

Input format (blank-line separated, optional category prefix):

    knowledge: She knows Mars is the fourth planet from the sun

    curiosity: She asked about earthquakes — what causes them

    personality: She drew a volcano with very precise layered details

If no category prefix, defaults to the --mind argument (knowledge).

Writes all candidates in a single atomic gate update.
Stages only; Record files are unchanged until companion approval and merge.

Usage:
    python scripts/batch_ingest_observations.py -u grace-mar < observations.txt
    python scripts/batch_ingest_observations.py -u grace-mar -f notes.txt
    python scripts/batch_ingest_observations.py -u grace-mar --dry-run < notes.txt
"""

from __future__ import annotations

import argparse
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

try:
    from stage_gate_candidate import (
        convergence_check,
        insert_before_processed,
        next_candidate_id,
        _candidate_ids,
        _slug_title,
        _yaml_double_quoted,
        _literal_block,
    )
    _HAS_STAGE = True
except ImportError:
    _HAS_STAGE = False

DEFAULT_USER = "grace-mar"

CATEGORY_MAP = {
    "knowledge": {
        "profile_target": "IX-A. KNOWLEDGE",
        "prompt_section": "YOUR KNOWLEDGE",
    },
    "curiosity": {
        "profile_target": "IX-B. CURIOSITY",
        "prompt_section": "YOUR CURIOSITY",
    },
    "personality": {
        "profile_target": "IX-C. PERSONALITY",
        "prompt_section": "YOUR PERSONALITY",
    },
}

_CATEGORY_PREFIX_RE = re.compile(
    r"^(knowledge|curiosity|personality)\s*:\s*", re.IGNORECASE,
)


# ---------------------------------------------------------------------------
# Inline fallbacks when stage_gate_candidate is unavailable (companion-self)
# ---------------------------------------------------------------------------

def _fb_candidate_ids(content: str) -> list[int]:
    return [int(m.group(1)) for m in re.finditer(r"\bCANDIDATE-(\d+)\b", content)]


def _fb_next_candidate_id(content: str) -> str:
    nums = _fb_candidate_ids(content)
    n = max(nums) + 1 if nums else 1
    return f"CANDIDATE-{n:04d}"


def _fb_slug_title(text: str, max_len: int = 56) -> str:
    one = " ".join(text.splitlines()[:1]).strip() or "batch observation"
    one = re.sub(r"\s+", " ", one)
    if len(one) > max_len:
        one = one[: max_len - 1].rstrip() + "\u2026"
    return one


def _fb_yaml_double_quoted(s: str) -> str:
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'


def _fb_literal_block(s: str, base_indent: str = "    ") -> str:
    if not s.strip():
        return base_indent + "(empty)\n"
    return "\n".join(base_indent + line for line in s.splitlines()) + "\n"


def _fb_insert_before_processed(full_md: str, block: str) -> str:
    m = re.search(r"^## Processed\s*$", full_md, re.MULTILINE)
    if not m:
        raise ValueError("recursion-gate.md must contain a ## Processed heading")
    return full_md[: m.start()] + block + full_md[m.start():]


_STOPWORDS = frozenset({
    "a", "an", "and", "are", "as", "be", "because", "for", "from", "has",
    "have", "how", "in", "is", "it", "its", "not", "of", "on", "or",
    "that", "the", "their", "this", "to", "was", "with", "you", "your",
})


def _tokenize(text: str) -> set[str]:
    return {t for t in re.findall(r"[a-z0-9]+", (text or "").lower())
            if len(t) >= 4 and t not in _STOPWORDS}


def _fb_convergence_check(
    gate_content: str,
    new_summary: str,
    new_body: str,
    *,
    min_overlap: int = 3,
) -> dict[str, object]:
    new_tokens = _tokenize(f"{new_summary} {new_body}")
    if not new_tokens:
        return {"sighting": "first", "prior_count": 0, "prior_ids": []}
    prior_ids: list[str] = []
    for m in re.finditer(
        r"### (CANDIDATE-\d+)(?:\s*\([^)]*\))?\s*\n```yaml\n(.*?)```",
        gate_content, re.DOTALL,
    ):
        existing = re.findall(r"(?:summary|suggested_entry|prompt_addition):\s*(.+)", m.group(2))
        existing_tokens = _tokenize(" ".join(existing))
        if len(new_tokens & existing_tokens) >= min_overlap:
            prior_ids.append(m.group(1))
    return {
        "sighting": "recurring" if prior_ids else "first",
        "prior_count": len(prior_ids),
        "prior_ids": prior_ids,
    }


# ---------------------------------------------------------------------------
# Resolve functions — prefer stage_gate_candidate imports, fall back inline
# ---------------------------------------------------------------------------

def _get_next_id(content: str) -> str:
    return next_candidate_id(content) if _HAS_STAGE else _fb_next_candidate_id(content)

def _get_id_nums(content: str) -> list[int]:
    return _candidate_ids(content) if _HAS_STAGE else _fb_candidate_ids(content)

def _get_slug(text: str) -> str:
    return _slug_title(text) if _HAS_STAGE else _fb_slug_title(text)

def _get_convergence(gc: str, s: str, b: str) -> dict:
    return convergence_check(gc, s, b) if _HAS_STAGE else _fb_convergence_check(gc, s, b)

def _do_insert(full: str, block: str) -> str:
    return insert_before_processed(full, block) if _HAS_STAGE else _fb_insert_before_processed(full, block)

def _dq(s: str) -> str:
    return _yaml_double_quoted(s) if _HAS_STAGE else _fb_yaml_double_quoted(s)

def _lb(s: str) -> str:
    return (_literal_block(s) if _HAS_STAGE else _fb_literal_block(s)).rstrip("\n")


# ---------------------------------------------------------------------------
# Core
# ---------------------------------------------------------------------------

def parse_observations(text: str, default_category: str = "knowledge") -> list[dict]:
    """Split input text into observation dicts with category and body."""
    blocks = re.split(r"\n\s*\n", text.strip())
    observations: list[dict] = []
    for block in blocks:
        block = block.strip()
        if not block:
            continue
        m = _CATEGORY_PREFIX_RE.match(block)
        if m:
            category = m.group(1).lower()
            body = block[m.end():].strip()
        else:
            category = default_category
            body = block
        if body:
            observations.append({"category": category, "body": body})
    return observations


def build_observation_block(
    *,
    candidate_id: str,
    body: str,
    mind_category: str,
    channel_key: str,
    timestamp: str,
    convergence: dict | None = None,
) -> str:
    cat = CATEGORY_MAP[mind_category]
    title = _get_slug(body)
    summary_text = body[:200].replace("\n", " ").strip()
    if len(body) > 200:
        summary_text = summary_text[:197] + "..."

    lines = [
        f"### {candidate_id} ({title})",
        "",
        "```yaml",
        "status: pending",
        f"timestamp: {timestamp}",
        f"channel_key: {channel_key}",
        "source: operator \u2014 scripts/batch_ingest_observations.py",
        "source_exchange:",
        "  operator: |",
        _lb(body),
        f"mind_category: {mind_category}",
        "signal_type: batch_observation",
        "priority_score: 3",
        f"summary: {_dq(summary_text)}",
    ]
    if convergence:
        sighting = convergence.get("sighting", "first")
        prior_ids = convergence.get("prior_ids", [])
        lines.append(f"convergence: {sighting}")
        if prior_ids:
            lines.append(f"convergence_prior: {', '.join(str(p) for p in prior_ids)}")
    lines.extend([
        f"profile_target: {cat['profile_target']}",
        f"suggested_entry: {_dq(body.strip()[:500])}",
        f"prompt_section: {cat['prompt_section']}",
        "prompt_addition: none",
        "```",
        "",
    ])
    return "\n".join(lines)


def batch_ingest(
    user_id: str,
    observations: list[dict],
    *,
    channel_key: str = "operator:cursor:batch-ingest",
    dry_run: bool = False,
) -> list[dict]:
    """Stage multiple observation candidates in one atomic write.

    Returns list of dicts with id, category, body, convergence per observation.
    """
    gate_path = REPO_ROOT / "users" / user_id / "recursion-gate.md"
    if not gate_path.is_file():
        print(f"ERROR: {gate_path} not found", file=sys.stderr)
        return []

    gate_content = gate_path.read_text(encoding="utf-8")
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    nums = _get_id_nums(gate_content)
    next_num = max(nums) + 1 if nums else 1

    results: list[dict] = []
    all_blocks: list[str] = []

    for obs in observations:
        cid = f"CANDIDATE-{next_num:04d}"
        conv = _get_convergence(gate_content, obs["body"], obs["body"])

        block = build_observation_block(
            candidate_id=cid,
            body=obs["body"],
            mind_category=obs["category"],
            channel_key=channel_key,
            timestamp=timestamp,
            convergence=conv,
        )

        all_blocks.append(block)
        results.append({
            "id": cid,
            "category": obs["category"],
            "body": obs["body"][:80],
            "convergence": conv.get("sighting", "first"),
        })
        next_num += 1

    combined = "\n".join(all_blocks)

    if dry_run:
        print("=== DRY RUN — blocks that would be staged ===\n")
        print(combined)
        print(f"\n=== {len(results)} observation(s) parsed ===")
    else:
        updated = _do_insert(gate_content, combined)
        gate_path.write_text(updated, encoding="utf-8")
        print(f"Staged {len(results)} observation(s) in {gate_path.name}:")
        for r in results:
            tag = f" [{r['convergence']}]" if r["convergence"] != "first" else ""
            print(f"  {r['id']} ({r['category']}){tag}: {r['body']}")

    return results


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Batch-stage observation candidates into recursion-gate.md",
    )
    ap.add_argument(
        "-u", "--user",
        default=os.getenv("GRACE_MAR_USER_ID", DEFAULT_USER).strip() or DEFAULT_USER,
    )
    ap.add_argument(
        "-f", "--file", type=Path, default=None,
        help="Read observations from file (default: stdin)",
    )
    ap.add_argument(
        "--mind",
        choices=("knowledge", "curiosity", "personality"),
        default="knowledge",
        help="Default mind_category when no prefix on a line (default: knowledge)",
    )
    ap.add_argument("--dry-run", action="store_true", help="Print blocks without writing")
    ap.add_argument(
        "--auto-score", action="store_true",
        help="After writing, run score_gate_candidates.py for this user",
    )
    ap.add_argument(
        "--channel-key", default="operator:cursor:batch-ingest",
        help="Override channel_key (default: operator:cursor:batch-ingest)",
    )
    args = ap.parse_args()

    if args.file:
        text = args.file.read_text(encoding="utf-8")
    else:
        if sys.stdin.isatty():
            print("Enter observations (blank line between entries, Ctrl-D to finish):")
        text = sys.stdin.read()

    observations = parse_observations(text, default_category=args.mind)
    if not observations:
        print("No observations found in input.", file=sys.stderr)
        return 1

    results = batch_ingest(
        args.user,
        observations,
        channel_key=args.channel_key,
        dry_run=args.dry_run,
    )

    if not args.dry_run and args.auto_score:
        score_script = REPO_ROOT / "scripts" / "score_gate_candidates.py"
        if score_script.is_file():
            import subprocess
            subprocess.run(
                [sys.executable, str(score_script), "-u", args.user],
                cwd=str(REPO_ROOT),
            )

    return 0 if results else 1


if __name__ == "__main__":
    sys.exit(main())

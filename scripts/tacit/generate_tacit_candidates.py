#!/usr/bin/env python3
"""
Generate review-only tacit candidate JSON files (non-canonical, deterministic heuristics).

Does not write recursion-gate.md or merge into the Record.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
SCHEMA_PATH = REPO_ROOT / "schema-registry" / "tacit-candidate.v1.json"
GENERATOR_VERSION = "1.0"

DEST_MAP = {
    "moonshot": "moonshot_insight_candidate",
    "skill": "skill_candidate",
    "library": "library_candidate",
    "work": "work_doctrine_candidate",
}

def _surface(ctype: str, lane: str) -> str:
    lane = lane or "work-*"
    m = {
        "moonshot_insight_candidate": "docs/skill-work/work-moonshots/missions/ (pick or create slug)",
        "skill_candidate": "skills-portable/ or .cursor/skills/ (operator choice)",
        "library_candidate": "users/<id>/SELF-LIBRARY/ (gate if promoted)",
        "work_doctrine_candidate": f"docs/skill-work/{lane}/ (WORK)",
    }
    return m[ctype]


def _snippet(text: str, n: int = 240) -> str:
    t = " ".join(text.split())
    return t if len(t) <= n else t[: n - 1] + "…"


def _review_questions(ctype: str) -> list[str]:
    common = [
        "Is the distilled claim accurate to the tacit note?",
        "Should this become a recursion-gate CANDIDATE-* or stay WORK-only?",
    ]
    extra = {
        "moonshot_insight_candidate": [
            "Which mission folder should own this if promoted?",
        ],
        "skill_candidate": [
            "Which portable skill or host skill should absorb this?",
        ],
        "library_candidate": [
            "Which LIB id or book scope does this belong to?",
        ],
        "work_doctrine_candidate": [
            "Which work lane README or doctrine file should reference this?",
        ],
    }
    return common + extra.get(ctype, [])


def _titles_for_type(ctype: str, excerpt: str) -> tuple[str, str]:
    base = excerpt[:80].strip() or "(empty tacit body)"
    title = base.split(".")[0][:72] if base else "Tacit candidate"
    if ctype == "moonshot_insight_candidate":
        return title, f"Mission-scale insight: {_snippet(excerpt)}"
    if ctype == "work_doctrine_candidate":
        return title, f"Work-lane doctrine note: {_snippet(excerpt)}"
    if ctype == "skill_candidate":
        return title, f"Skill-relevant pattern: {_snippet(excerpt)}"
    return title, f"Library-relevant note: {_snippet(excerpt)}"


def generate_from_normalized(record: dict[str, Any]) -> list[dict[str, Any]]:
    tacit_id = record["id"]
    norm_path = record["provenance_path"]
    lane = str(record.get("lane") or "")
    raw = record.get("raw_text") or ""
    excerpt = _snippet(raw)
    conf = record.get("confidence") or "medium"
    dests = [d.strip().lower() for d in record.get("candidate_destinations") or []]

    types_emitted: list[str] = []
    out: list[dict[str, Any]] = []
    for d in dests:
        ctype = DEST_MAP.get(d)
        if not ctype or ctype in types_emitted:
            continue
        types_emitted.append(ctype)
        title, claim = _titles_for_type(ctype, raw)
        cand: dict[str, Any] = {
            "candidate_type": ctype,
            "title": title,
            "distilled_claim": claim,
            "rationale": f"Derived from tacit destination '{d}' and lane '{lane}'.",
            "supporting_excerpts": [excerpt],
            "proposed_destination_surface": _surface(ctype, lane),
            "confidence": conf,
            "review_questions": _review_questions(ctype),
            "provenance_tacit_id": tacit_id,
            "provenance_normalized_path": norm_path,
            "generator_version": GENERATOR_VERSION,
        }
        out.append(cand)

    if not out and "moonshot" in raw.lower():
        ctype = "moonshot_insight_candidate"
        title, claim = _titles_for_type(ctype, raw)
        out.append(
            {
                "candidate_type": ctype,
                "title": title,
                "distilled_claim": claim,
                "rationale": "Inferred from keyword 'moonshot' in raw text (no explicit destination).",
                "supporting_excerpts": [excerpt],
                "proposed_destination_surface": _surface(ctype, lane),
                "confidence": conf,
                "review_questions": _review_questions(ctype),
                "provenance_tacit_id": tacit_id,
                "provenance_normalized_path": norm_path,
                "generator_version": GENERATOR_VERSION,
            }
        )

    return out


def _validate_one(cand: dict[str, Any]) -> list[str]:
    try:
        from jsonschema import Draft202012Validator
    except ImportError:
        return []
    if not SCHEMA_PATH.is_file():
        return [f"missing schema {SCHEMA_PATH}"]
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema)
    return [str(e.message) for e in sorted(validator.iter_errors(cand), key=lambda e: e.path)]


def main() -> int:
    ap = argparse.ArgumentParser(description="Generate tacit candidate JSON files.")
    ap.add_argument("--normalized", "-n", type=Path, required=True, help="Normalized tacit JSON path")
    ap.add_argument(
        "--output-dir",
        "-o",
        type=Path,
        default=None,
        help="Output directory (default: <repo>/runtime/tacit/candidates)",
    )
    ap.add_argument("--stdout", action="store_true", help="Print JSON array to stdout only")
    ap.add_argument("--repo-root", type=Path, default=REPO_ROOT)
    args = ap.parse_args()

    root = args.repo_root.resolve()
    npath = args.normalized.resolve()
    record = json.loads(npath.read_text(encoding="utf-8"))
    candidates = generate_from_normalized(record)

    if args.stdout:
        print(json.dumps(candidates, indent=2, ensure_ascii=False))
        return 0

    out_dir = (args.output_dir or (root / "runtime" / "tacit" / "candidates")).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    tacit_id = record["id"]
    safe = re.sub(r"[^a-zA-Z0-9_.-]+", "_", tacit_id)

    for i, cand in enumerate(candidates):
        errs = _validate_one(cand)
        if errs:
            for e in errs:
                print(f"schema: {e}", file=sys.stderr)
            return 3
        suffix = cand["candidate_type"].replace("_candidate", "")
        fname = f"{safe}_{suffix}.json"
        op = out_dir / fname
        op.write_text(json.dumps(cand, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"wrote {op}", file=sys.stderr)

    if not candidates:
        print("(no candidates generated)", file=sys.stderr)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Archive a winning experiment artifact under accepted/."""

from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

SELF_PROPOSALS_DIR = Path(__file__).resolve().parent
EXPERIMENTS_DIR = SELF_PROPOSALS_DIR / "experiments"
ACCEPTED_DIR = SELF_PROPOSALS_DIR / "accepted"
ARTIFACT_SCHEMA_VERSION = 1


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _proposal_fingerprint(proposal: dict) -> str:
    payload = json.dumps(proposal, sort_keys=True, ensure_ascii=True)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def _best_existing_scalar(directory: Path) -> float | None:
    best: float | None = None
    for path in sorted(directory.glob("*.json")):
        try:
            payload = _load_json(path)
        except json.JSONDecodeError:
            continue
        scalar = payload.get("score_bundle", {}).get("scalar")
        if isinstance(scalar, (int, float)):
            value = float(scalar)
            if best is None or value > best:
                best = value
    return best


def _fingerprint_exists(directory: Path, fingerprint: str) -> bool:
    for path in sorted(directory.glob("*.json")):
        try:
            payload = _load_json(path)
        except json.JSONDecodeError:
            continue
        if payload.get("proposal_fingerprint") == fingerprint:
            return True
    return False


def main() -> int:
    parser = argparse.ArgumentParser(description="Archive a winning self-proposal experiment.")
    parser.add_argument(
        "--input",
        type=Path,
        default=EXPERIMENTS_DIR / "last_score.json",
        help="Path to a prepare.py result JSON",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Archive even if the scalar is not better than the current best accepted artifact",
    )
    parser.add_argument(
        "--min-scalar",
        type=float,
        default=0.0,
        help="Minimum scalar required before the artifact can be archived",
    )
    parser.add_argument(
        "--min-delta",
        type=float,
        default=None,
        help="Minimum improvement required over the current best accepted artifact",
    )
    args = parser.parse_args()

    if not args.input.is_file():
        raise SystemExit(f"Missing input score file: {args.input}")

    payload = _load_json(args.input)
    score_bundle = payload.get("score_bundle", {})
    scalar = score_bundle.get("scalar")
    proposal = payload.get("proposal")
    if not score_bundle.get("ok"):
        raise SystemExit("Refusing to archive a failed score bundle")
    if not isinstance(scalar, (int, float)):
        raise SystemExit("Input file missing score_bundle.scalar")
    if not isinstance(proposal, dict):
        raise SystemExit("Input file missing proposal payload")
    if float(scalar) < float(args.min_scalar):
        raise SystemExit(
            f"Refusing to archive: scalar {float(scalar):.4f} is below --min-scalar {float(args.min_scalar):.4f}"
        )

    ACCEPTED_DIR.mkdir(parents=True, exist_ok=True)
    current_best = _best_existing_scalar(ACCEPTED_DIR)
    delta = None if current_best is None else float(scalar) - current_best
    if args.min_delta is not None and current_best is not None and delta < float(args.min_delta):
        raise SystemExit(
            f"Refusing to archive: delta {delta:.4f} is below --min-delta {float(args.min_delta):.4f}"
        )
    fingerprint = _proposal_fingerprint(proposal)
    if _fingerprint_exists(ACCEPTED_DIR, fingerprint) and not args.force:
        raise SystemExit("Refusing to archive duplicate proposal_fingerprint without --force")
    if current_best is not None and float(scalar) <= current_best and not args.force:
        print(
            f"Not archived: scalar {float(scalar):.4f} is not better than current best {current_best:.4f}. Use --force to keep anyway."
        )
        return 1

    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    out_path = ACCEPTED_DIR / f"accepted-{ts}.json"
    candidate_bundle = proposal.get("candidate_bundle", {})
    artifact = {
        "artifact_schema_version": ARTIFACT_SCHEMA_VERSION,
        "accepted_at": datetime.now(timezone.utc).isoformat(),
        "accepted_for": "research_only",
        "operator_warning": "accepted for research, not approved for Record",
        "source_score_file": str(args.input),
        "best_before_accept": current_best,
        "scalar_at_accept": float(scalar),
        "score_components": score_bundle.get("components", {}),
        "hard_gates": score_bundle.get("hard_gates", {}),
        "raw_source_exchange": candidate_bundle.get("source_exchange", {}),
        "proposal_projection": {
            "summary": candidate_bundle.get("summary", ""),
            "suggested_entry": candidate_bundle.get("suggested_entry", ""),
            "prompt_addition": candidate_bundle.get("prompt_addition", ""),
        },
        "proposal_fingerprint": fingerprint,
        **payload,
    }
    out_path.write_text(json.dumps(artifact, indent=2) + "\n", encoding="utf-8")
    print(out_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""
Semantic consistency checks for seed intent vs readiness (beyond JSON Schema).

Fails (exit 1) when readiness claims pass but intent is too vague, workflows
contradict, or readiness_score is below a typical activation band.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

MIN_PURPOSE_LEN = 40
PASS_MIN_READINESS_SCORE = 0.75


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser(description="Check seed_intent vs seed_readiness consistency.")
    parser.add_argument("directory", type=Path, help="seed-phase directory")
    args = parser.parse_args()

    d = args.directory.resolve()
    intent_path = d / "seed_intent.json"
    readiness_path = d / "seed_readiness.json"
    if not intent_path.is_file() or not readiness_path.is_file():
        print("Missing seed_intent.json or seed_readiness.json", file=sys.stderr)
        return 1

    intent = load_json(intent_path)
    readiness = load_json(readiness_path)
    rd = readiness.get("readiness") or {}

    semantic_errors: list[str] = []

    purpose = (intent.get("companion_purpose") or "").strip()
    if len(purpose) < MIN_PURPOSE_LEN:
        semantic_errors.append(
            f"companion_purpose is too short ({len(purpose)} chars; need at least {MIN_PURPOSE_LEN}) "
            "to count as sufficiently specific."
        )

    supported = set(intent.get("supported_workflows") or [])
    unsupported = set(intent.get("unsupported_workflows") or [])
    overlap = sorted(supported & unsupported)
    if overlap:
        semantic_errors.append(f"supported/unsupported workflow overlap: {', '.join(overlap)}")

    decision = rd.get("decision")
    score = rd.get("readiness_score")

    if decision == "pass":
        if semantic_errors:
            for e in semantic_errors:
                print(e, file=sys.stderr)
            print(
                "readiness decision is pass but semantic consistency checks failed.",
                file=sys.stderr,
            )
            return 1
        if isinstance(score, (int, float)) and score < PASS_MIN_READINESS_SCORE:
            print(
                f"readiness decision is pass but readiness_score {score} is below "
                f"typical activation threshold ({PASS_MIN_READINESS_SCORE}).",
                file=sys.stderr,
            )
            return 1

    if semantic_errors:
        for e in semantic_errors:
            print(e, file=sys.stderr)
        print(
            "(Non-fatal: readiness decision is not pass; fix before seeking activation.)",
            file=sys.stderr,
        )

    print("OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

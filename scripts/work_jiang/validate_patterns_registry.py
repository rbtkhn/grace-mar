#!/usr/bin/env python3
"""Validate pattern-tracking/registry/patterns.jsonl — IDs, joins to predictions, recurrence invariants."""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
WORK_JIANG = ROOT / "research" / "external" / "work-jiang"
PATTERNS_PATH = WORK_JIANG / "pattern-tracking" / "registry" / "patterns.jsonl"
PREDICTIONS_PATH = WORK_JIANG / "prediction-tracking" / "registry" / "predictions.jsonl"

PATTERN_ID_RE = re.compile(r"^pat-\d{4,}$")
PREDICTION_ID_RE = re.compile(r"^jiang-[A-Za-z0-9]+-\d{3}$")


def load_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        return []
    rows: list[dict] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        rows.append(json.loads(line))
    return rows


def load_prediction_ids() -> set[str]:
    ids: set[str] = set()
    for row in load_jsonl(PREDICTIONS_PATH):
        pid = row.get("prediction_id")
        if isinstance(pid, str) and pid:
            ids.add(pid)
    return ids


def validate_patterns(
    patterns: list[dict],
    prediction_ids: set[str],
) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    seen_ids: set[str] = set()
    all_pattern_ids = {p.get("pattern_id") for p in patterns if p.get("pattern_id")}

    for i, row in enumerate(patterns):
        loc = f"line {i + 1}"
        pid = row.get("pattern_id")
        if not pid or not isinstance(pid, str):
            errors.append(f"{loc}: missing pattern_id")
            continue
        if not PATTERN_ID_RE.match(pid):
            errors.append(
                f"{loc}: pattern_id '{pid}' must match pat-NNNN... (zero-padded, min 4 digits)"
            )
        if pid in seen_ids:
            errors.append(f"{loc}: duplicate pattern_id '{pid}'")
        seen_ids.add(pid)

        name = row.get("name", "")
        if not isinstance(name, str) or len(name.strip()) < 3:
            errors.append(f"{loc} ({pid}): name too short or missing")

        definition = row.get("definition", "")
        if not isinstance(definition, str) or len(definition.strip()) < 40:
            errors.append(f"{loc} ({pid}): definition too short or missing (min ~40 chars)")

        sigs = row.get("observable_signatures")
        if not isinstance(sigs, list) or len(sigs) < 1:
            errors.append(f"{loc} ({pid}): observable_signatures must be a non-empty list")
        elif not all(isinstance(s, str) and s.strip() for s in sigs):
            errors.append(f"{loc} ({pid}): observable_signatures must be non-empty strings")

        perf = row.get("performance")
        if not isinstance(perf, dict):
            errors.append(f"{loc} ({pid}): performance must be an object")
            continue

        nar = perf.get("narrative", "")
        if not isinstance(nar, str) or len(nar.strip()) < 20:
            errors.append(f"{loc} ({pid}): performance.narrative too short or missing")

        sm = perf.get("signatures_matched")
        tc = perf.get("total_cases")
        if not isinstance(sm, int) or sm < 0:
            errors.append(f"{loc} ({pid}): performance.signatures_matched must be int >= 0")
        if not isinstance(tc, int) or tc < 1:
            errors.append(f"{loc} ({pid}): performance.total_cases must be int >= 1")
        if isinstance(sm, int) and isinstance(tc, int) and sm > tc:
            errors.append(
                f"{loc} ({pid}): signatures_matched ({sm}) cannot exceed total_cases ({tc})"
            )

        rec = perf.get("recurrence")
        if rec is not None:
            if not isinstance(rec, dict):
                errors.append(f"{loc} ({pid}): performance.recurrence must be an object or omitted")
            else:
                lo = rec.get("lecture_occurrences", 0)
                ao = rec.get("analog_occurrences", 0)
                if not isinstance(lo, int) or lo < 0:
                    errors.append(
                        f"{loc} ({pid}): recurrence.lecture_occurrences must be int >= 0"
                    )
                if not isinstance(ao, int) or ao < 0:
                    errors.append(
                        f"{loc} ({pid}): recurrence.analog_occurrences must be int >= 0"
                    )
                fq = rec.get("frequency_qualifier")
                allowed_fq = (
                    "high",
                    "medium",
                    "low",
                    "rare",
                    "context-dependent",
                )
                if fq is not None and fq not in allowed_fq:
                    errors.append(
                        f"{loc} ({pid}): recurrence.frequency_qualifier must be one of {allowed_fq}"
                    )
                if isinstance(lo, int) and isinstance(ao, int) and isinstance(tc, int):
                    if lo + ao > tc:
                        errors.append(
                            f"{loc} ({pid}): lecture_occurrences ({lo}) + analog_occurrences ({ao}) "
                            f"cannot exceed total_cases ({tc})"
                        )
                    if isinstance(sm, int) and lo + ao > sm:
                        warnings.append(
                            f"{loc} ({pid}): lecture_occurrences + analog_occurrences ({lo + ao}) "
                            f"> signatures_matched ({sm}) — check semantics or document in note"
                        )

        for lp in row.get("linked_prediction_ids") or []:
            if not isinstance(lp, str):
                errors.append(f"{loc} ({pid}): linked_prediction_ids must be strings")
                continue
            if not PREDICTION_ID_RE.match(lp):
                warnings.append(
                    f"{loc} ({pid}): linked_prediction_id '{lp}' does not match jiang-*-NNN pattern"
                )
            if prediction_ids and lp not in prediction_ids:
                errors.append(
                    f"{loc} ({pid}): linked_prediction_id '{lp}' not in predictions.jsonl"
                )

        for dep in row.get("dependencies") or []:
            if not isinstance(dep, str):
                errors.append(f"{loc} ({pid}): dependencies must be strings")
            elif dep not in all_pattern_ids:
                errors.append(
                    f"{loc} ({pid}): dependency '{dep}' is not a pattern_id in this registry"
                )

        hooks = row.get("evidence_hooks") or []
        if hooks:
            for h in hooks:
                if not isinstance(h, dict):
                    errors.append(f"{loc} ({pid}): evidence_hooks entries must be objects")
                    continue
                if not (h.get("video_id") or h.get("lecture_ref") or h.get("source_id")):
                    errors.append(
                        f"{loc} ({pid}): each evidence_hook needs video_id, lecture_ref, or source_id"
                    )

        if (
            isinstance(tc, int)
            and tc > 1
            and isinstance(sm, int)
            and sm > 0
            and not rec
        ):
            warnings.append(
                f"{loc} ({pid}): performance.recurrence recommended when total_cases > 1 "
                f"and signatures_matched > 0 (lecture vs analog split)"
            )

    return errors, warnings


def run_validation() -> tuple[list[str], list[str]]:
    patterns = load_jsonl(PATTERNS_PATH)
    pred_ids = load_prediction_ids()
    return validate_patterns(patterns, pred_ids)


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument(
        "--json",
        action="store_true",
        help="Print errors/warnings as JSON to stdout",
    )
    args = p.parse_args()

    if not PATTERNS_PATH.exists():
        print(f"Missing {PATTERNS_PATH.relative_to(ROOT)}", file=sys.stderr)
        return 1

    errors, warnings = run_validation()
    if args.json:
        print(json.dumps({"errors": errors, "warnings": warnings}, indent=2))
    else:
        for w in warnings:
            print(f"WARNING: {w}", file=sys.stderr)
        for e in errors:
            print(f"ERROR: {e}", file=sys.stderr)
        if not errors and not warnings:
            print(f"OK — {PATTERNS_PATH.relative_to(ROOT)}")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())

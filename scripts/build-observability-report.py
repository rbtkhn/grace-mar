#!/usr/bin/env python3
"""
Build observability-report.json from Change Proposal v1 files under review-queue/proposals/
and subprocess validation results.

Reads proposal fields: status, primaryScope, secondaryScopes, targetSurface, changeType,
supportingEvidence[].type, createdAt.

Default review root: users/demo/review-queue
Default output: users/demo/observability/observability-report.json

Validates output against schema-registry/observability-report.v1.json when present and jsonschema is installed.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

try:
    import jsonschema
except ImportError:
    jsonschema = None  # type: ignore


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schema-registry" / "observability-report.v1.json"

STATUS_KEYS = [
    "proposed",
    "under_review",
    "approved",
    "deferred",
    "rejected",
    "superseded",
]

# CamelCase report keys for proposalCounts (aligned with observability-report.v1.json)
STATUS_TO_REPORT = {
    "proposed": "proposed",
    "under_review": "underReview",
    "approved": "approved",
    "deferred": "deferred",
    "rejected": "rejected",
    "superseded": "superseded",
}


def load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def run_validator(script: str, args: List[str]) -> tuple[int, str]:
    cmd = [sys.executable, str(ROOT / "scripts" / script), *args]
    try:
        proc = subprocess.run(
            cmd,
            cwd=str(ROOT),
            capture_output=True,
            text=True,
            timeout=120,
        )
        err = (proc.stderr or "") + (proc.stdout or "")
        return proc.returncode, err.strip()
    except Exception as exc:  # noqa: BLE001
        return 99, str(exc)


def parse_iso(dt: str) -> Optional[datetime]:
    if not dt or not isinstance(dt, str):
        return None
    try:
        if dt.endswith("Z"):
            dt = dt[:-1] + "+00:00"
        return datetime.fromisoformat(dt.replace("Z", "+00:00"))
    except ValueError:
        return None


def main() -> int:
    parser = argparse.ArgumentParser(description="Build observability-report.json for a review-queue tree.")
    parser.add_argument(
        "--review-root",
        default="users/demo/review-queue",
        help="Path to review-queue directory (default: users/demo/review-queue)",
    )
    parser.add_argument(
        "--output",
        default="",
        help="Output JSON path (default: users/demo/observability/observability-report.json)",
    )
    parser.add_argument(
        "--skip-seed-validation",
        action="store_true",
        help="Do not run validate-seed-phase.py on users/demo/seed-phase",
    )
    parser.add_argument(
        "--seed-phase-dir",
        default="users/demo/seed-phase",
        help="Seed phase dir for optional validation (default: users/demo/seed-phase)",
    )
    parser.add_argument(
        "--stale-days",
        type=int,
        default=14,
        help="Days after which proposed/under_review proposals count as stale (default: 14)",
    )
    parser.add_argument(
        "--no-schema-validate",
        action="store_true",
        help="Skip validating output against observability-report.v1.json",
    )
    args = parser.parse_args()

    review_root = (ROOT / args.review_root).resolve()
    proposals_dir = review_root / "proposals"
    if not proposals_dir.is_dir():
        print(f"ERROR: proposals directory not found: {proposals_dir}", file=sys.stderr)
        return 1

    out_path = Path(args.output) if args.output else ROOT / "users/demo/observability/observability-report.json"
    out_path = out_path.resolve()
    out_path.parent.mkdir(parents=True, exist_ok=True)

    status_counts: Counter = Counter()
    change_type_counts: Counter = Counter()
    target_surface_counts: Counter = Counter()
    scope_counts: Counter = Counter()
    evidence_type_counts: Counter = Counter()
    stale_count = 0
    now = datetime.now(timezone.utc)
    stale_delta_days = args.stale_days

    for fp in sorted(proposals_dir.glob("*.json")):
        if not fp.is_file():
            continue
        try:
            obj = load_json(fp)
        except (json.JSONDecodeError, OSError):
            continue
        st = obj.get("status")
        if st in STATUS_KEYS:
            status_counts[st] += 1
        else:
            status_counts["unknown"] += 1

        ct = obj.get("changeType")
        if isinstance(ct, str):
            change_type_counts[ct] += 1

        ts = obj.get("targetSurface")
        if isinstance(ts, str):
            target_surface_counts[ts] += 1

        ps = obj.get("primaryScope")
        if isinstance(ps, str):
            scope_counts[ps] += 1
        for s in obj.get("secondaryScopes") or []:
            if isinstance(s, str):
                scope_counts[s] += 1

        for ev in obj.get("supportingEvidence") or []:
            if isinstance(ev, dict):
                t = ev.get("type")
                if isinstance(t, str):
                    evidence_type_counts[t] += 1

        if st in ("proposed", "under_review"):
            created = parse_iso(str(obj.get("createdAt") or ""))
            if created is not None:
                if created.tzinfo is None:
                    created = created.replace(tzinfo=timezone.utc)
                age = (now - created).days
                if age >= stale_delta_days:
                    stale_count += 1

    proposal_counts_report = {STATUS_TO_REPORT[s]: int(status_counts.get(s, 0)) for s in STATUS_KEYS}
    if status_counts.get("unknown", 0):
        proposal_counts_report["unknownStatus"] = int(status_counts["unknown"])

    # validate-change-review on this review root
    rel_review = str(review_root.relative_to(ROOT))
    cr_args = [rel_review]
    if "/_template/" in f"/{rel_review}/":
        cr_args.append("--allow-empty")
    cr_code, cr_err = run_validator("validate-change-review.py", cr_args)

    change_review_passed = cr_code == 0

    seed_ran = False
    seed_passed = False
    seed_code: Optional[int] = None
    seed_err = ""
    if not args.skip_seed_validation:
        seed_path = ROOT / args.seed_phase_dir
        if seed_path.is_dir():
            rel_seed = str(seed_path.relative_to(ROOT))
            seed_ran = True
            seed_code, seed_err = run_validator("validate-seed-phase.py", [rel_seed])
            seed_passed = seed_code == 0

    seed_block: Dict[str, Any] = {
        "ran": seed_ran,
        "exitCode": seed_code if seed_ran else None,
        "passed": seed_passed if seed_ran else False,
        "detail": seed_err[:2000] if seed_err else "",
    }

    report: Dict[str, Any] = {
        "schemaVersion": "1.0.0",
        "generatedAt": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "reviewRoot": str(Path(args.review_root).as_posix()),
        "proposalCounts": proposal_counts_report,
        "changeTypeCounts": dict(change_type_counts),
        "targetSurfaceCounts": dict(target_surface_counts),
        "scopeCounts": dict(scope_counts),
        "evidenceTypeCounts": dict(evidence_type_counts),
        "staleReviewCount": stale_count,
        "validationSummary": {
            "changeReview": {
                "ran": True,
                "exitCode": cr_code,
                "passed": change_review_passed,
                "detail": cr_err[:2000] if cr_err else "",
            },
            "seedPhaseDemo": seed_block,
        },
    }

    text = json.dumps(report, indent=2, ensure_ascii=False) + "\n"
    out_path.write_text(text, encoding="utf-8")

    if not args.no_schema_validate and jsonschema is not None and SCHEMA_PATH.is_file():
        schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
        jsonschema.validate(instance=report, schema=schema)

    print(out_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

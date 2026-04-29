#!/usr/bin/env python3
"""Work-strategy packet validators: structural integrity checks (WORK-only, stdlib)."""

from __future__ import annotations

import argparse
import json
import re
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from packet_common import (
    MIN_WORDS_NON_TRIVIAL,
    is_forbidden_record_path,
    is_text_like,
    safe_rel,
    word_count,
)

SCHEMA_VERSION = "work-strategy-validation-report.v1"
LANE = "work-strategy"

UNRESOLVED_MARKERS = ["TODO", "TBD", "UNRESOLVED", "NEEDS REVIEW", "???"]
CONTRADICTION_MARKERS = ["contradiction", "conflict", "in tension", "uncertain"]
HEADING_PATTERN = re.compile(r"^\s{0,3}#{1,6}\s+\S", re.MULTILINE)


def read_text_if_possible(path: Path) -> str | None:
    if not path.is_file():
        return None
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None


def scan_markers(text: str, markers: list[str]) -> dict[str, Any]:
    by_marker: dict[str, int] = {}
    total = 0
    lower = text.lower()
    for m in markers:
        if m == "???":
            c = text.count("???")
        else:
            c = lower.count(m.lower())
        by_marker[m] = c
        total += c
    return {"by_marker": by_marker, "total_hits": total}


def summarize_validator_status(validators: list[dict[str, Any]]) -> str:
    statuses = [v["status"] for v in validators]
    if "fail" in statuses:
        return "fail"
    if "needs_review" in statuses:
        return "needs_review"
    return "pass"


def validate_packet(
    *,
    repo_root: Path,
    task_arg: str | None,
    sources: list[str],
    artifacts: list[str],
    gate_snippet_arg: str | None,
    run_id: str,
    validation_out_path: Path | None,
    created_at: str | None = None,
) -> dict[str, Any]:
    """Build validation report dict (no file I/O except reading inputs)."""
    root = repo_root.resolve()
    ts = created_at or datetime.now(timezone.utc).isoformat()

    def resolve_arg(p: str) -> Path:
        pp = Path(p)
        return (root / pp).resolve() if not pp.is_absolute() else pp.resolve()

    sources_resolved = [resolve_arg(s) for s in sources]
    artifacts_resolved = [resolve_arg(a) for a in artifacts]

    validators_out: list[dict[str, Any]] = []

    # E — record boundary on validation output path
    out_forbidden = False
    out_notes = ""
    if validation_out_path is None:
        validators_out.append(
            {
                "id": "record_boundary_guard",
                "label": "Validation report output path allowed",
                "status": "pass",
                "details": "No --out; report returned in-memory / stdout only.",
                "subject_paths": [],
            }
        )
    else:
        out_forbidden = is_forbidden_record_path(validation_out_path, root)
        rel_out = safe_rel(validation_out_path, root)
        if out_forbidden:
            validators_out.append(
                {
                    "id": "record_boundary_guard",
                    "label": "Validation report output path allowed",
                    "status": "fail",
                    "details": f"Forbidden output path: {rel_out}",
                    "subject_paths": [rel_out],
                }
            )
            out_notes = "Validation JSON output path is forbidden."
        else:
            validators_out.append(
                {
                    "id": "record_boundary_guard",
                    "label": "Validation report output path allowed",
                    "status": "pass",
                    "details": rel_out,
                    "subject_paths": [rel_out],
                }
            )

    # A — required artifacts present (paths explicitly passed via --artifact)
    missing_artifacts = [safe_rel(p, root) for p in artifacts_resolved if not p.is_file()]
    if missing_artifacts:
        validators_out.append(
            {
                "id": "required_artifacts_present",
                "label": "Expected artifact paths exist",
                "status": "fail",
                "details": "Missing: " + ", ".join(missing_artifacts),
                "subject_paths": missing_artifacts,
            }
        )
    else:
        validators_out.append(
            {
                "id": "required_artifacts_present",
                "label": "Expected artifact paths exist",
                "status": "pass",
                "details": f"{len(artifacts_resolved)} artifact path(s) present.",
                "subject_paths": [safe_rel(p, root) for p in artifacts_resolved],
            }
        )

    # B — sources present
    missing_sources = [safe_rel(p, root) for p in sources_resolved if not p.is_file()]
    if missing_sources:
        validators_out.append(
            {
                "id": "sources_present",
                "label": "Declared source paths exist",
                "status": "needs_review",
                "details": "Missing sources: " + ", ".join(missing_sources),
                "subject_paths": missing_sources,
            }
        )
    else:
        validators_out.append(
            {
                "id": "sources_present",
                "label": "Declared source paths exist",
                "status": "pass",
                "details": f"{len(sources_resolved)} source path(s).",
                "subject_paths": [safe_rel(p, root) for p in sources_resolved],
            }
        )

    # C — artifact substance (text-like word counts)
    existing_text_paths: list[tuple[Path, str]] = []
    for ap in artifacts_resolved:
        if not ap.is_file():
            continue
        if is_text_like(ap):
            raw = read_text_if_possible(ap)
            if raw is not None:
                existing_text_paths.append((ap, raw))

    if not artifacts_resolved:
        validators_out.append(
            {
                "id": "artifact_substance",
                "label": "Artifact substance (text word-count heuristic)",
                "status": "fail",
                "details": "No artifacts declared (--artifact empty).",
                "subject_paths": [],
            }
        )
    elif not existing_text_paths:
        validators_out.append(
            {
                "id": "artifact_substance",
                "label": "Artifact substance (text word-count heuristic)",
                "status": "needs_review",
                "details": "No readable text/markdown artifacts for word count.",
                "subject_paths": [safe_rel(p, root) for p in artifacts_resolved],
            }
        )
    else:
        word_counts = [(p, word_count(t)) for p, t in existing_text_paths]
        any_strong = any(wc >= MIN_WORDS_NON_TRIVIAL for _, wc in word_counts)
        if any_strong:
            validators_out.append(
                {
                    "id": "artifact_substance",
                    "label": "Artifact substance (text word-count heuristic)",
                    "status": "pass",
                    "details": f"At least one text artifact >= {MIN_WORDS_NON_TRIVIAL} words.",
                    "subject_paths": [safe_rel(p, root) for p, _ in existing_text_paths],
                }
            )
        else:
            thin_detail = "; ".join(f"{safe_rel(p, root)} ({wc} words)" for p, wc in word_counts)
            validators_out.append(
                {
                    "id": "artifact_substance",
                    "label": "Artifact substance (text word-count heuristic)",
                    "status": "needs_review",
                    "details": "All text artifacts below threshold: " + thin_detail,
                    "subject_paths": [safe_rel(p, root) for p, _ in existing_text_paths],
                }
            )

    # D — gate snippet
    if not gate_snippet_arg:
        validators_out.append(
            {
                "id": "gate_snippet_present",
                "label": "Gate snippet requested and usable",
                "status": "pass",
                "details": "Gate snippet not requested (--gate-snippet omitted).",
                "subject_paths": [],
            }
        )
    else:
        gp = resolve_arg(gate_snippet_arg)
        gtxt = read_text_if_possible(gp)
        if not gtxt or not gtxt.strip():
            validators_out.append(
                {
                    "id": "gate_snippet_present",
                    "label": "Gate snippet requested and usable",
                    "status": "needs_review",
                    "details": "Gate snippet missing, unreadable, or empty.",
                    "subject_paths": [safe_rel(gp, root)],
                }
            )
        else:
            validators_out.append(
                {
                    "id": "gate_snippet_present",
                    "label": "Gate snippet requested and usable",
                    "status": "pass",
                    "details": f"{len(gtxt.strip())} non-whitespace characters.",
                    "subject_paths": [safe_rel(gp, root)],
                }
            )

    # F — unresolved markers in artifact bodies
    combined_artifact_text = "\n\n".join(t for _, t in existing_text_paths)
    unr = scan_markers(combined_artifact_text, UNRESOLVED_MARKERS)
    if unr["total_hits"] > 0:
        validators_out.append(
            {
                "id": "unresolved_marker_scan",
                "label": "Unresolved / placeholder markers in artifacts",
                "status": "needs_review",
                "details": json.dumps(unr["by_marker"], ensure_ascii=False),
                "subject_paths": [safe_rel(p, root) for p, _ in existing_text_paths],
            }
        )
    else:
        validators_out.append(
            {
                "id": "unresolved_marker_scan",
                "label": "Unresolved / placeholder markers in artifacts",
                "status": "pass",
                "details": "No TODO/TBD/UNRESOLVED/NEEDS REVIEW/??? hits in scanned artifact text.",
                "subject_paths": [],
            }
        )

    # G — contradiction / tension markers
    ctr = scan_markers(combined_artifact_text, CONTRADICTION_MARKERS)
    if ctr["total_hits"] > 0:
        validators_out.append(
            {
                "id": "contradiction_marker_scan",
                "label": "Explicit tension / uncertainty markers",
                "status": "needs_review",
                "details": json.dumps(ctr["by_marker"], ensure_ascii=False),
                "subject_paths": [safe_rel(p, root) for p, _ in existing_text_paths],
            }
        )
    else:
        validators_out.append(
            {
                "id": "contradiction_marker_scan",
                "label": "Explicit tension / uncertainty markers",
                "status": "pass",
                "details": "No contradiction/conflict/in tension/uncertain substring hits.",
                "subject_paths": [],
            }
        )

    # H — markdown heading check (light)
    heading_issues: list[str] = []
    for ap, raw in existing_text_paths:
        if ap.suffix.lower() not in {".md", ".markdown"}:
            continue
        wc = word_count(raw)
        if wc == 0:
            continue
        if not HEADING_PATTERN.search(raw):
            if wc >= 20:
                heading_issues.append(safe_rel(ap, root))

    if heading_issues:
        validators_out.append(
            {
                "id": "markdown_heading_metadata",
                "label": "Markdown artifacts have at least one heading",
                "status": "needs_review",
                "details": "Substantial markdown without heading: " + ", ".join(heading_issues),
                "subject_paths": heading_issues,
            }
        )
    else:
        validators_out.append(
            {
                "id": "markdown_heading_metadata",
                "label": "Markdown artifacts have at least one heading",
                "status": "pass",
                "details": "No problematic markdown structure detected for scanned files.",
                "subject_paths": [],
            }
        )

    summary_status = summarize_validator_status(validators_out)
    passed = sum(1 for v in validators_out if v["status"] == "pass")
    failed = sum(1 for v in validators_out if v["status"] == "fail")
    nr = sum(1 for v in validators_out if v["status"] == "needs_review")
    summary_notes = (
        f"validators: pass={passed} fail={failed} needs_review={nr}"
        + (f"; {out_notes}" if out_notes else "")
    )

    target_obj: dict[str, Any] = {
        "task": task_arg,
        "sources": list(sources),
        "artifacts": list(artifacts),
        "gate_snippet": gate_snippet_arg,
        "validation_out": safe_rel(validation_out_path, root) if validation_out_path else None,
    }

    report = {
        "schema_version": SCHEMA_VERSION,
        "run_id": run_id,
        "created_at": ts,
        "lane": LANE,
        "target": target_obj,
        "validators": validators_out,
        "summary": {
            "status": summary_status,
            "passed": passed,
            "failed": failed,
            "needs_review": nr,
            "notes": summary_notes.strip(),
        },
        "record_boundary": {
            "canonical_paths_written": [],
            "canonical_write_violation": bool(validation_out_path and out_forbidden),
            "notes": "Validators emit derived JSON only; they do not mutate Record or gate staging.",
        },
    }
    return report


def run_validate_cli(args: argparse.Namespace) -> tuple[dict[str, Any], int]:
    repo_root = Path(args.repo_root).resolve()
    run_id = args.run_id or str(uuid.uuid4())
    created_at = datetime.now(timezone.utc).isoformat()

    out_resolved: Path | None = None
    if args.out:
        out_resolved = (
            (repo_root / args.out).resolve()
            if not Path(args.out).is_absolute()
            else Path(args.out).resolve()
        )

    report = validate_packet(
        repo_root=repo_root,
        task_arg=args.task,
        sources=list(args.source or []),
        artifacts=list(args.artifact or []),
        gate_snippet_arg=args.gate_snippet,
        run_id=run_id,
        validation_out_path=out_resolved,
        created_at=created_at,
    )

    exit_code = 0
    st = report["summary"]["status"]
    mode = args.fail_on_status
    if mode == "fail":
        exit_code = 1 if st == "fail" else 0
    elif mode == "needs_review":
        exit_code = 1 if st in ("fail", "needs_review") else 0
    else:
        exit_code = 0

    if out_resolved and not report["record_boundary"]["canonical_write_violation"]:
        out_resolved.parent.mkdir(parents=True, exist_ok=True)
        rel_out = safe_rel(out_resolved, repo_root)
        report["record_boundary"]["canonical_paths_written"] = [rel_out]
        out_resolved.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    elif out_resolved and report["record_boundary"]["canonical_write_violation"]:
        exit_code = max(exit_code, 1)

    return report, exit_code


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Work-strategy strategy packet validators (WORK-only).")
    p.add_argument("--task", type=str, default=None, help="Task intake path (recorded in report target).")
    p.add_argument("--source", action="append", default=[], help="Source path (repeatable).")
    p.add_argument("--artifact", action="append", default=[], help="Artifact path (repeatable).")
    p.add_argument("--gate-snippet", type=str, default=None, help="Optional gate snippet path.")
    p.add_argument("--out", type=str, default=None, help="Validation JSON output path.")
    p.add_argument("--run-id", type=str, default=None, dest="run_id")
    p.add_argument("--repo-root", type=str, default=None, dest="repo_root")
    p.add_argument("--json", action="store_true", help="Print validation report JSON to stdout.")
    p.add_argument(
        "--fail-on-status",
        choices=("fail", "needs_review", "never"),
        default="fail",
        dest="fail_on_status",
        help="Exit nonzero policy (default: nonzero when overall status is fail).",
    )
    args = p.parse_args(argv)
    root = args.repo_root or Path(__file__).resolve().parent.parent.parent
    args.repo_root = str(Path(root).resolve())
    return args


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    report, exit_code = run_validate_cli(args)
    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    elif report["record_boundary"].get("canonical_write_violation"):
        print("Validators refused forbidden --out path.", file=sys.stderr)
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())

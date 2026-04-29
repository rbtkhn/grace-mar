#!/usr/bin/env python3
"""Work-strategy carry harness: intake + artifact checks -> JSON receipt (WORK-only, stdlib)."""

from __future__ import annotations

import argparse
import importlib.util
import json
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from packet_common import (
    MIN_WORDS_NON_TRIVIAL,
    inspect_artifact,
    is_forbidden_record_path,
    is_text_like,
    safe_rel as _safe_rel,
    word_count,
)

HARNESS_NAME = "run_carry_harness"
HARNESS_VERSION = "1.0.0"
SCHEMA_VERSION = "work-strategy-carry-receipt.v1"


def _load_validator_module() -> Any:
    """Load validate_strategy_packet from this directory (supports importlib tests)."""
    root = Path(__file__).resolve().parent
    ws = str(root)
    if ws not in sys.path:
        sys.path.insert(0, ws)
    path = root / "validate_strategy_packet.py"
    spec = importlib.util.spec_from_file_location("validate_strategy_packet", path)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def determine_result(checks: list[dict[str, Any]]) -> str:
    statuses = [c["status"] for c in checks]
    if "fail" in statuses:
        return "fail"
    if "needs_review" in statuses:
        return "needs_review"
    return "pass"


def build_receipt(
    *,
    run_id: str,
    created_at: str,
    task_path: Path | None,
    task_text: str,
    source_paths: list[str],
    artifact_paths: list[str],
    gate_snippet_path: Path | None,
    gate_snippet_text: str,
    repo_root: Path,
    observed: list[dict[str, Any]],
    checks: list[dict[str, Any]],
    output_forbidden: bool,
    receipt_out_path: Path | None,
    validation_report_path: str | None,
    validation_summary: dict[str, Any] | None,
) -> dict[str, Any]:
    summary_counts = {"pass": 0, "fail": 0, "needs_review": 0}
    for c in checks:
        summary_counts[c["status"]] += 1
    result = determine_result(checks)
    notes_parts = [
        f"checks: pass={summary_counts['pass']} fail={summary_counts['fail']} needs_review={summary_counts['needs_review']}"
    ]
    if output_forbidden:
        notes_parts.append("Output path is forbidden; receipt file not written.")

    gate_ready = bool(gate_snippet_path and gate_snippet_text.strip())

    receipt: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "run_id": run_id,
        "created_at": created_at,
        "lane": "work-strategy",
        "harness": {"name": HARNESS_NAME, "version": HARNESS_VERSION},
        "input": {
            "task_title": task_text.splitlines()[0][:200] if task_text else "",
            "task_path": _safe_rel(task_path, repo_root) if task_path and task_path.is_file() else None,
            "task_text_preview": task_text[:2000] if task_text else "",
            "source_paths": list(source_paths),
            "artifact_paths": list(artifact_paths),
            "gate_snippet_path": _safe_rel(gate_snippet_path, repo_root) if gate_snippet_path else None,
        },
        "expected_artifacts": [{"path": p} for p in artifact_paths],
        "observed_artifacts": observed,
        "checks": checks,
        "summary": {
            "status": result,
            "passed": summary_counts["pass"],
            "failed": summary_counts["fail"],
            "needs_review": summary_counts["needs_review"],
            "notes": " ".join(notes_parts),
        },
        "gate_snippet": {
            "ready": gate_ready,
            "text": gate_snippet_text if gate_ready else "",
            "notes": "Paste-only; not staged or approved."
            if gate_snippet_path
            else "No gate snippet path provided.",
        },
        "record_boundary": {
            "canonical_paths_written": [],
            "canonical_write_violation": output_forbidden,
            "notes": "Harness does not write users/, bot/prompt.py, bot/bot.py, bot/wechat_bot.py."
            + (" Attempted forbidden receipt path." if output_forbidden else ""),
        },
        "result": result,
    }
    if validation_report_path is not None or validation_summary is not None:
        receipt["validation_report_path"] = validation_report_path
        receipt["validation_summary"] = validation_summary
    return receipt


def run_harness(args: argparse.Namespace) -> tuple[dict[str, Any], int]:
    repo_root = Path(args.repo_root).resolve()
    run_id = args.run_id or str(uuid.uuid4())
    created_at = datetime.now(timezone.utc).isoformat()

    task_text = ""
    task_path: Path | None = None
    if args.task:
        task_path = (repo_root / args.task).resolve() if not Path(args.task).is_absolute() else Path(args.task).resolve()
        if not task_path.is_file():
            task_text = ""
        else:
            try:
                task_text = task_path.read_text(encoding="utf-8", errors="replace")
            except OSError:
                task_text = ""

    sources_resolved = [
        (repo_root / p).resolve() if not Path(p).is_absolute() else Path(p).resolve()
        for p in (args.source or [])
    ]
    artifacts_resolved = [
        (repo_root / p).resolve() if not Path(p).is_absolute() else Path(p).resolve()
        for p in (args.artifact or [])
    ]

    gate_path: Path | None = None
    gate_text = ""
    if args.gate_snippet:
        gate_path = (
            (repo_root / args.gate_snippet).resolve()
            if not Path(args.gate_snippet).is_absolute()
            else Path(args.gate_snippet).resolve()
        )
        if gate_path.is_file():
            try:
                gate_text = gate_path.read_text(encoding="utf-8", errors="replace")
            except OSError:
                gate_text = ""

    out_arg = args.out
    receipt_out = (
        (repo_root / out_arg).resolve()
        if out_arg and not Path(out_arg).is_absolute()
        else Path(out_arg).resolve()
        if out_arg
        else None
    )

    output_forbidden = bool(receipt_out and is_forbidden_record_path(receipt_out, repo_root))

    validation_report_path_val: str | None = None
    validation_summary_val: dict[str, Any] | None = None
    validation_out_resolved: Path | None = None
    validation_output_forbidden = False

    if getattr(args, "run_validators", False):
        vr_arg = getattr(args, "validation_report", None)
        if vr_arg:
            validation_out_resolved = (
                (repo_root / vr_arg).resolve()
                if not Path(vr_arg).is_absolute()
                else Path(vr_arg).resolve()
            )
            validation_output_forbidden = is_forbidden_record_path(validation_out_resolved, repo_root)

        vmod = _load_validator_module()
        v_report = vmod.validate_packet(
            repo_root=repo_root,
            task_arg=args.task,
            sources=list(args.source or []),
            artifacts=list(args.artifact or []),
            gate_snippet_arg=args.gate_snippet,
            run_id=run_id,
            validation_out_path=validation_out_resolved,
            created_at=created_at,
        )
        summ = v_report.get("summary") or {}
        validation_summary_val = {
            "status": summ.get("status", "pass"),
            "passed": summ.get("passed", 0),
            "failed": summ.get("failed", 0),
            "needs_review": summ.get("needs_review", 0),
            "notes": summ.get("notes", ""),
        }
        if validation_out_resolved and not validation_output_forbidden:
            validation_report_path_val = _safe_rel(validation_out_resolved, repo_root)
            validation_out_resolved.parent.mkdir(parents=True, exist_ok=True)
            rb = v_report.setdefault("record_boundary", {})
            if isinstance(rb, dict):
                rb["canonical_paths_written"] = [validation_report_path_val]
                rb["canonical_write_violation"] = False
            validation_out_resolved.write_text(
                json.dumps(v_report, indent=2, ensure_ascii=False) + "\n",
                encoding="utf-8",
            )
        elif validation_out_resolved and validation_output_forbidden:
            validation_summary_val["notes"] = (
                validation_summary_val.get("notes", "")
                + " Validation report path forbidden; JSON not written."
            ).strip()

    checks: list[dict[str, Any]] = []

    # task_readable
    if not args.task:
        checks.append(
            {
                "id": "task_readable",
                "label": "Task file provided and readable",
                "status": "fail",
                "details": "Missing --task.",
            }
        )
    elif not task_path or not task_path.is_file():
        checks.append(
            {
                "id": "task_readable",
                "label": "Task file provided and readable",
                "status": "fail",
                "details": f"Task not found: {args.task}",
            }
        )
    else:
        checks.append(
            {
                "id": "task_readable",
                "label": "Task file provided and readable",
                "status": "pass",
                "details": _safe_rel(task_path, repo_root),
            }
        )

    # sources_present
    missing_sources = [_safe_rel(p, repo_root) for p in sources_resolved if not p.is_file()]
    if missing_sources:
        checks.append(
            {
                "id": "sources_present",
                "label": "All source paths exist",
                "status": "needs_review",
                "details": "Missing: " + ", ".join(missing_sources),
            }
        )
    else:
        checks.append(
            {
                "id": "sources_present",
                "label": "All source paths exist",
                "status": "pass",
                "details": str(len(sources_resolved)) + " source(s).",
            }
        )

    observed: list[dict[str, Any]] = []
    for ap in artifacts_resolved:
        obs = inspect_artifact(ap, repo_root)
        observed.append(obs)

    missing_art = [_safe_rel(p, repo_root) for p, o in zip(artifacts_resolved, observed, strict=True) if not o.get("exists")]
    if missing_art:
        checks.append(
            {
                "id": "artifacts_exist",
                "label": "All expected artifact paths exist",
                "status": "fail",
                "details": "Missing: " + ", ".join(missing_art),
            }
        )
    else:
        checks.append(
            {
                "id": "artifacts_exist",
                "label": "All expected artifact paths exist",
                "status": "pass",
                "details": str(len(artifacts_resolved)) + " artifact(s).",
            }
        )

    # artifact weight (text-like only)
    thin: list[str] = []
    text_seen = False
    strong = False
    for p, o in zip(artifacts_resolved, observed, strict=True):
        if not o.get("exists"):
            continue
        if is_text_like(p):
            text_seen = True
            wc = o.get("word_count", 0)
            if isinstance(wc, int) and wc >= MIN_WORDS_NON_TRIVIAL:
                strong = True
            elif isinstance(wc, int):
                thin.append(f"{o['path']} ({wc} words)")
    if missing_art:
        artifact_weight_status = "pass"
        artifact_weight_detail = "Skipped (missing artifacts)."
    elif not artifacts_resolved:
        artifact_weight_status = "pass"
        artifact_weight_detail = "No artifacts declared."
    elif text_seen and strong:
        artifact_weight_status = "pass"
        artifact_weight_detail = f"At least one text artifact >= {MIN_WORDS_NON_TRIVIAL} words."
    elif text_seen and thin:
        artifact_weight_status = "needs_review"
        artifact_weight_detail = "Thin text artifacts: " + "; ".join(thin)
    else:
        artifact_weight_status = "needs_review"
        artifact_weight_detail = "No qualifying text artifacts for word-count heuristic."

    checks.append(
        {
            "id": "artifact_weight",
            "label": f"Text artifacts non-trivial (>={MIN_WORDS_NON_TRIVIAL} words)",
            "status": artifact_weight_status,
            "details": artifact_weight_detail,
        }
    )

    if args.gate_snippet:
        if not gate_path or not gate_path.is_file():
            checks.append(
                {
                    "id": "gate_snippet_nonempty",
                    "label": "Gate snippet exists and non-empty",
                    "status": "needs_review",
                    "details": "Gate snippet path missing or unreadable.",
                }
            )
        elif not gate_text.strip():
            checks.append(
                {
                    "id": "gate_snippet_nonempty",
                    "label": "Gate snippet exists and non-empty",
                    "status": "needs_review",
                    "details": "Gate snippet file is empty.",
                }
            )
        else:
            checks.append(
                {
                    "id": "gate_snippet_nonempty",
                    "label": "Gate snippet exists and non-empty",
                    "status": "pass",
                    "details": f"{len(gate_text)} characters.",
                }
            )

    if receipt_out:
        if output_forbidden:
            checks.append(
                {
                    "id": "output_path_safe",
                    "label": "Receipt output path allowed",
                    "status": "fail",
                    "details": f"Forbidden output path: {_safe_rel(receipt_out, repo_root)}",
                }
            )
        else:
            checks.append(
                {
                    "id": "output_path_safe",
                    "label": "Receipt output path allowed",
                    "status": "pass",
                    "details": _safe_rel(receipt_out, repo_root),
                }
            )
    else:
        checks.append(
            {
                "id": "output_path_safe",
                "label": "Receipt output path allowed",
                "status": "fail",
                "details": "Missing --out.",
            }
        )

    receipt = build_receipt(
        run_id=run_id,
        created_at=created_at,
        task_path=task_path,
        task_text=task_text,
        source_paths=[str(Path(p).as_posix()) for p in (args.source or [])],
        artifact_paths=[str(Path(p).as_posix()) for p in (args.artifact or [])],
        gate_snippet_path=gate_path,
        gate_snippet_text=gate_text,
        repo_root=repo_root,
        observed=observed,
        checks=checks,
        output_forbidden=output_forbidden,
        receipt_out_path=receipt_out,
        validation_report_path=validation_report_path_val,
        validation_summary=validation_summary_val,
    )

    exit_code = 0
    res = receipt["result"]
    mode = args.fail_on_result
    if mode == "fail":
        exit_code = 1 if res == "fail" else 0
    elif mode == "needs_review":
        exit_code = 1 if res in ("fail", "needs_review") else 0
    else:
        exit_code = 0

    if receipt_out and not output_forbidden:
        receipt_out.parent.mkdir(parents=True, exist_ok=True)
        receipt_out.write_text(json.dumps(receipt, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    return receipt, exit_code


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Work-strategy carry harness (WORK-only receipt).")
    p.add_argument("--task", type=str, help="Path to task intake markdown.")
    p.add_argument("--out", type=str, required=True, help="Receipt JSON output path.")
    p.add_argument("--source", action="append", default=[], help="Source path (repeatable).")
    p.add_argument("--artifact", action="append", default=[], help="Expected artifact path (repeatable).")
    p.add_argument("--gate-snippet", type=str, default=None, help="Optional gate snippet markdown/text.")
    p.add_argument("--run-id", type=str, default=None, dest="run_id")
    p.add_argument("--repo-root", type=str, default=None, dest="repo_root")
    p.add_argument("--json", action="store_true", help="Print receipt JSON to stdout.")
    p.add_argument(
        "--fail-on-result",
        choices=("fail", "needs_review", "never"),
        default="fail",
        help="Exit nonzero policy (default: nonzero only when result is fail).",
    )
    p.add_argument(
        "--run-validators",
        action="store_true",
        help="Run validate_strategy_packet and optionally embed validation summary + write JSON report.",
    )
    p.add_argument(
        "--validation-report",
        type=str,
        default=None,
        dest="validation_report",
        help="Path for validation JSON when --run-validators is set.",
    )
    args = p.parse_args(argv)
    root = args.repo_root or Path(__file__).resolve().parent.parent.parent
    args.repo_root = str(Path(root).resolve())
    return args


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    receipt, exit_code = run_harness(args)
    if args.json:
        print(json.dumps(receipt, indent=2, ensure_ascii=False))
    elif receipt["record_boundary"]["canonical_write_violation"]:
        print("Harness refused forbidden --out path.", file=sys.stderr)
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())

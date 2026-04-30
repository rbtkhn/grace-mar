#!/usr/bin/env python3
"""Repo-owned entrypoint for derived artifact regeneration."""

from __future__ import annotations

import argparse
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

from derived_regeneration import (
    DEFAULT_RECEIPT_DIR,
    REPO_ROOT,
    TARGETS,
    TARGETS_BY_ID,
    build_rationale_payload,
    cleanup_owned_outputs,
    default_receipt_path,
    detect_git_changed_paths,
    expand_with_downstream,
    matched_paths_for_target,
    normalize_rel_path,
    sidecar_path_for_artifact,
    select_targets_for_paths,
    topologically_sort_targets,
    write_receipt,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument(
        "--changed",
        action="store_true",
        help="select targets from changed paths (default behavior when no mode is given)",
    )
    mode.add_argument(
        "--all",
        action="store_true",
        help="run all known rebuild targets",
    )
    mode.add_argument(
        "--target",
        action="append",
        default=None,
        metavar="TARGET_ID",
        help="run specific target ids (repeatable)",
    )
    parser.add_argument(
        "--paths",
        action="append",
        default=None,
        metavar="PATH",
        help="repo-relative changed path (repeat or comma-separated); default: detect from git status",
    )
    parser.add_argument(
        "--user",
        default="grace-mar",
        help="user id for user-scoped generators (default: grace-mar)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="print matched targets and commands without executing them",
    )
    parser.add_argument(
        "--incremental",
        action="store_true",
        help="expand changed targets to downstream dependents and run in dependency order",
    )
    parser.add_argument(
        "--receipt-output",
        type=Path,
        default=None,
        help="receipt path; default: artifacts/work-dev/rebuild-receipts/derived-rebuild-YYYYMMDD-HHMMSS.json",
    )
    parser.add_argument(
        "--no-receipt",
        action="store_true",
        help="do not write a receipt JSON",
    )
    return parser


def _expand(values: list[str] | None) -> list[str]:
    if not values:
        return []
    out: list[str] = []
    for value in values:
        for part in value.split(","):
            stripped = part.strip()
            if stripped:
                out.append(normalize_rel_path(stripped))
    return out


def _runtime_command(cmd: list[str]) -> list[str]:
    if cmd and cmd[0] == "python3":
        return [sys.executable, *cmd[1:]]
    return cmd


def _selected_targets(args: argparse.Namespace, changed_paths: list[str]):
    if args.all:
        return topologically_sort_targets(list(TARGETS)), "all"
    if args.target:
        selected = []
        for target_id in args.target:
            if target_id not in TARGETS_BY_ID:
                raise SystemExit(f"unknown target id: {target_id}")
            selected.append(TARGETS_BY_ID[target_id])
        return topologically_sort_targets(selected), "targeted"
    selected = select_targets_for_paths(changed_paths)
    if args.incremental:
        selected = expand_with_downstream(selected)
        return topologically_sort_targets(selected), "incremental"
    return topologically_sort_targets(selected), "changed"


def _build_receipt_payload(
    *,
    now: datetime,
    mode: str,
    user: str,
    changed_paths: list[str],
    target_rows: list[dict],
    overall_status: str,
) -> dict:
    return {
        "receiptKind": "derived_rebuild",
        "receiptId": f"drb-{now:%Y%m%d-%H%M%S}",
        "createdAt": now.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "mode": mode,
        "user": user,
        "changedPaths": changed_paths,
        "targets": target_rows,
        "resultStatus": overall_status,
        "recordAuthority": "none",
        "gateEffect": "none",
    }


def main() -> int:
    args = build_parser().parse_args()
    changed_paths = _expand(args.paths) or detect_git_changed_paths(REPO_ROOT)
    selected, mode = _selected_targets(args, changed_paths)

    now = datetime.now(timezone.utc)
    receipt_path = None
    if not args.no_receipt:
        if args.receipt_output is None:
            receipt_path = default_receipt_path(receipt_dir=DEFAULT_RECEIPT_DIR, now=now)
        else:
            receipt_path = args.receipt_output
            if not receipt_path.is_absolute():
                receipt_path = REPO_ROOT / receipt_path

    target_rows: list[dict] = []
    overall_status = "noop"

    if not selected:
        print("No derived rebuild targets selected.")
    for target in selected:
        commands = target.commands_for_user(args.user)
        outputs = target.outputs_for_user(args.user)
        matched_paths = matched_paths_for_target(changed_paths, target)
        rationale_sidecars = [sidecar_path_for_artifact(output) for output in outputs]
        row: dict[str, object] = {
            "targetId": target.target_id,
            "description": target.description,
            "producerScript": target.producer_script,
            "policyMode": target.policy_mode,
            "matchedPaths": matched_paths,
            "commands": [" ".join(cmd) for cmd in commands],
            "outputs": outputs,
            "rationaleSidecars": rationale_sidecars,
        }
        if args.dry_run:
            row["status"] = "dry_run"
            print(f"[dry-run] {target.target_id}")
            for cmd in commands:
                print(f"  {' '.join(cmd)}")
            target_rows.append(row)
            overall_status = "dry_run"
            continue

        overall_status = "ok"
        start = time.monotonic()
        cleaned_outputs = cleanup_owned_outputs(REPO_ROOT, target=target, user=args.user)
        if cleaned_outputs:
            row["cleanedOwnedOutputs"] = cleaned_outputs
        for cmd in commands:
            print(f"[run] {' '.join(cmd)}", flush=True)
            proc = subprocess.run(
                _runtime_command(cmd),
                cwd=REPO_ROOT,
                capture_output=True,
                text=True,
            )
            if proc.stdout.strip():
                print(proc.stdout.rstrip())
            if proc.returncode != 0:
                if proc.stderr.strip():
                    print(proc.stderr.rstrip(), file=sys.stderr)
                row["status"] = "failed"
                row["returnCode"] = proc.returncode
                row["stderrTail"] = proc.stderr[-4000:]
                row["elapsedMs"] = int((time.monotonic() - start) * 1000)
                target_rows.append(row)
                overall_status = "failed"
                if receipt_path is not None:
                    payload = _build_receipt_payload(
                        now=now,
                        mode=mode,
                        user=args.user,
                        changed_paths=changed_paths,
                        target_rows=target_rows,
                        overall_status=overall_status,
                    )
                    write_receipt(receipt_path, payload)
                    print(f"wrote receipt: {receipt_path}")
                return proc.returncode
        missing_outputs = [
            output for output in outputs if not (REPO_ROOT / output).is_file()
        ]
        if missing_outputs:
            row["status"] = "failed"
            row["missingOutputs"] = missing_outputs
            row["elapsedMs"] = int((time.monotonic() - start) * 1000)
            target_rows.append(row)
            overall_status = "failed"
            if receipt_path is not None:
                payload = _build_receipt_payload(
                    now=now,
                    mode=mode,
                    user=args.user,
                    changed_paths=changed_paths,
                    target_rows=target_rows,
                    overall_status=overall_status,
                )
                write_receipt(receipt_path, payload)
                print(f"wrote receipt: {receipt_path}")
            print(
                f"missing expected outputs for {target.target_id}: {', '.join(missing_outputs)}",
                file=sys.stderr,
            )
            return 1
        written_sidecars: list[str] = []
        generated_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        rationale_inputs = matched_paths if mode in {"changed", "incremental"} else []
        for output in outputs:
            sidecar_rel = sidecar_path_for_artifact(output)
            payload = build_rationale_payload(
                target=target,
                user=args.user,
                artifact_path=output,
                generated_at=generated_at,
                matched_paths=rationale_inputs,
            )
            write_receipt(REPO_ROOT / sidecar_rel, payload)
            written_sidecars.append(sidecar_rel)
        row["status"] = "ok"
        row["elapsedMs"] = int((time.monotonic() - start) * 1000)
        row["writtenRationaleSidecars"] = written_sidecars
        target_rows.append(row)

    if receipt_path is not None:
        payload = _build_receipt_payload(
            now=now,
            mode=mode,
            user=args.user,
            changed_paths=changed_paths,
            target_rows=target_rows,
            overall_status=overall_status,
        )
        write_receipt(receipt_path, payload)
        print(f"wrote receipt: {receipt_path}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

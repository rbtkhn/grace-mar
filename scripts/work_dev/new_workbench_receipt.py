#!/usr/bin/env python3
"""
Create a new Workbench Harness receipt JSON (WORKBENCH-RECEIPT-SPEC v0.1).

Default output:
  artifacts/work-dev/workbench-receipts/workbench-YYYYMMDD-HHMMSS.json

Does not stage to recursion-gate or touch Record surfaces.

Usage (from repo root):
  python3 scripts/work_dev/new_workbench_receipt.py --artifact-type react \\
    --candidate-id A --source-prompt-ref docs/.../x.md --launch-command "npm run dev"
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

from validate_workbench_receipt import ALLOWED_STATUS

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
DEFAULT_RECEIPT_DIR = REPO_ROOT / "artifacts" / "work-dev" / "workbench-receipts"

_FORBIDDEN_NAMES = frozenset(
    {
        "self.md",
        "self-archive.md",
        "self-library.md",
        "recursion-gate.md",
    }
)


def _expand_list(values: list[str] | None) -> list[str]:
    if not values:
        return []
    out: list[str] = []
    for v in values:
        for part in v.split(","):
            p = part.strip()
            if p:
                out.append(p)
    return out


def _forbidden_write_path(path: Path) -> bool:
    try:
        resolved = path.resolve()
        rel = resolved.relative_to(REPO_ROOT)
    except ValueError:
        return False
    if len(rel.parts) >= 2 and rel.parts[0] == "users" and rel.name in _FORBIDDEN_NAMES:
        return True
    return False


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument(
        "--artifact-type",
        default="unspecified",
        help="maps to artifactType (default: %(default)s)",
    )
    p.add_argument(
        "--candidate-id",
        default="",
        help="maps to artifactCandidateLabel (not a gate CANDIDATE id)",
    )
    p.add_argument(
        "--source-prompt-ref",
        default="",
        help="prompt, session, or doc ref",
    )
    p.add_argument(
        "--paths-touched",
        action="append",
        default=None,
        metavar="PATH",
        help="repo-relative path (repeat or comma-separated)",
    )
    p.add_argument(
        "--commands-run",
        action="append",
        default=None,
        metavar="CMD",
        help="shell command (repeat or comma-separated)",
    )
    p.add_argument(
        "--launch-command",
        default="",
        help="command used to start the artifact",
    )
    p.add_argument(
        "--inspection-method",
        default="pending",
        help="inspection.method when not yet run (default: pending)",
    )
    p.add_argument(
        "--screenshots",
        action="append",
        default=None,
        metavar="PATH",
        help="repo-relative screenshot paths (repeat or comma-separated)",
    )
    p.add_argument(
        "--observed-failures",
        action="append",
        default=None,
        metavar="TEXT",
        help="inspection failure notes (repeat or comma-separated)",
    )
    p.add_argument(
        "--acceptance-checklist",
        action="append",
        default=None,
        metavar="TEXT",
        help="checklist lines (repeat or comma-separated)",
    )
    p.add_argument(
        "--revision-summary",
        default="",
        help="what changed this round",
    )
    p.add_argument(
        "--status",
        default="draft",
        choices=sorted(ALLOWED_STATUS),
        help="workflow status (default: draft)",
    )
    p.add_argument(
        "--lane",
        default="work-dev",
        help="harness lane (default: work-dev)",
    )
    p.add_argument(
        "--receipt-id",
        default="",
        help="if omitted, derived as wb-YYYYMMDD-HHMMSS (UTC, aligned with default filename stamp)",
    )
    p.add_argument(
        "--workbench-run-id",
        default="",
        help="if omitted, set to same as receiptId",
    )
    p.add_argument(
        "--output",
        "-o",
        type=Path,
        default=None,
        help="output JSON; relative paths resolve to repo root; "
        "default: artifacts/work-dev/workbench-receipts/workbench-YYYYMMDD-HHMMSS.json",
    )
    p.add_argument(
        "--meta-note",
        default="",
        help="optional top-level metaNote",
    )
    return p


def main() -> int:
    ns = build_parser().parse_args()
    now = datetime.now(timezone.utc)
    stamp = now.strftime("%Y%m%d-%H%M%S")

    if ns.output is None:
        out_path = DEFAULT_RECEIPT_DIR / f"workbench-{stamp}.json"
    else:
        out_path = ns.output
        if not out_path.is_absolute():
            out_path = REPO_ROOT / out_path

    rid = ns.receipt_id or f"wb-{stamp}"
    run_id = ns.workbench_run_id or rid
    created = now.strftime("%Y-%m-%dT%H:%M:%SZ")
    rec: dict = {
        "receiptKind": "workbench",
        "receiptId": rid,
        "createdAt": created,
        "workbenchRunId": run_id,
        "lane": ns.lane,
        "artifactType": ns.artifact_type,
        "artifactCandidateLabel": ns.candidate_id,
        "relatedGateCandidateId": None,
        "sourcePromptRef": ns.source_prompt_ref,
        "pathsTouched": _expand_list(ns.paths_touched),
        "commandsRun": _expand_list(ns.commands_run),
        "launchCommand": ns.launch_command,
        "inspection": {
            "method": ns.inspection_method,
            "screenshots": _expand_list(ns.screenshots),
            "observedFailures": _expand_list(ns.observed_failures),
            "acceptanceChecklist": _expand_list(ns.acceptance_checklist),
        },
        "revisionSummary": ns.revision_summary,
        "status": ns.status,
        "recordAuthority": "none",
        "gateEffect": "none",
    }
    if ns.meta_note:
        rec["metaNote"] = ns.meta_note

    if _forbidden_write_path(out_path):
        print(
            f"refuse: will not write to protected path: {out_path}",
            file=sys.stderr,
        )
        return 1
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(
        json.dumps(rec, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(f"wrote: {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

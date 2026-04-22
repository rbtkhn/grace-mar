#!/usr/bin/env python3
"""
Runtime worker peer review — heuristic pass on a draft proposal + execution receipt.

Distinct from review_orchestrator.py (observations / gate packet path). Runtime-only;
does not merge, stage, or alter RECURSION-GATE.

Usage:
  python3 scripts/runtime/run_runtime_peer_review.py --draft-run-id rw_... --task-file task.txt
  python3 scripts/runtime/run_runtime_peer_review.py --draft-run-id rw_... --task "..." --save
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
PEER_SCHEMA_PATH = REPO_ROOT / "schema-registry" / "runtime-peer-review.v1.json"
EXECUTION_RECEIPT_SCHEMA_PATH = REPO_ROOT / "schema-registry" / "execution-receipt.v1.json"

_FORBIDDEN_HINTS = (
    "users/grace-mar/self.md",
    "users/grace-mar/recursion-gate.md",
    "users/grace-mar/self-archive.md",
    "bot/prompt.py",
)


def _worker_home(repo_root: Path) -> Path:
    raw = os.environ.get("GRACE_MAR_RUNTIME_WORKER_HOME", "").strip()
    if raw:
        return Path(raw).expanduser().resolve()
    return (repo_root / "runtime" / "runtime-worker").resolve()


def _peer_run_id() -> str:
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    h = hashlib.sha256(f"{ts}:{uuid.uuid4().hex}".encode()).hexdigest()[:12]
    return f"pr_{ts}_{h}"


def _repo_rel(path: Path, repo_root: Path) -> str:
    try:
        return path.resolve().relative_to(repo_root.resolve()).as_posix()
    except ValueError:
        return str(path.resolve())


def _validate(instance: dict[str, Any], schema_path: Path) -> None:
    try:
        import jsonschema
    except ImportError:
        return
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    jsonschema.Draft202012Validator(schema).validate(instance)


def _heuristic_verdict(
    *,
    draft_text: str,
    receipt: dict[str, Any],
) -> tuple[str, list[str], dict[str, Any], dict[str, Any]]:
    flags: list[str] = []
    low = draft_text.lower()
    for s in _FORBIDDEN_HINTS:
        if s in low or s in draft_text:
            flags.append(f"draft_mentions_forbidden_path:{s}")

    sv = receipt.get("scope_verification")
    overdetail: str | None = None
    detected = False
    if isinstance(sv, dict) and sv.get("status") == "overclaim_suspected":
        detected = True
        overdetail = "scope_verification.status is overclaim_suspected"
    elif isinstance(sv, dict) and sv.get("warnings"):
        w = sv.get("warnings") or []
        if any("exceeds opened" in str(x) for x in w):
            detected = True
            overdetail = "scope_verification warnings indicate stated > opened"

    epi = receipt.get("epistemic") or {}
    decision = str(epi.get("decision") or "")

    notes: list[str] = []
    if decision:
        notes.append(f"draft_receipt epistemic.decision={decision}")
    if isinstance(sv, dict) and sv.get("status"):
        notes.append(f"scope_verification.status={sv.get('status')}")

    if flags:
        verdict = "flagged"
    elif detected:
        verdict = "flagged"
    elif decision in ("hold", "block", "abstain"):
        verdict = "hold"
    elif decision == "allow_with_review":
        verdict = "review_recommended"
    else:
        verdict = "ok"

    ev_ass = "sufficient" if not flags and not detected and decision in ("allow", "allow_with_review") else "needs_caution"

    return verdict, flags, {
        "detected": detected,
        "detail": overdetail,
    }, {
        "assessment": ev_ass,
        "notes": notes,
    }


def build_peer_review(
    *,
    repo_root: Path,
    draft_run_id: str,
    original_task: str,
    review_run_id: str,
    review_artifact_relpath: str | None,
) -> dict[str, Any]:
    wh = _worker_home(repo_root)
    receipt_p = wh / "receipts" / f"{draft_run_id}.json"
    proposal_p = wh / "proposals" / f"{draft_run_id}.md"
    if not receipt_p.is_file():
        raise FileNotFoundError(f"draft receipt not found: {receipt_p}")
    if not proposal_p.is_file():
        raise FileNotFoundError(f"draft proposal not found: {proposal_p}")

    receipt = json.loads(receipt_p.read_text(encoding="utf-8"))
    draft_text = proposal_p.read_text(encoding="utf-8")

    draft_out_rel = _repo_rel(proposal_p, repo_root)
    draft_rec_rel = _repo_rel(receipt_p, repo_root)

    v, flags, overclaim, ev = _heuristic_verdict(draft_text=draft_text, receipt=receipt)
    if review_artifact_relpath is not None:
        linkage_r = review_artifact_relpath
    else:
        linkage_r = None
    return {
        "schema_version": "1.0-runtime-peer-review",
        "non_canonical": True,
        "review_run_id": review_run_id,
        "draft_run_id": draft_run_id,
        "linkage": {
            "draft_receipt_relpath": draft_rec_rel,
            "review_artifact_relpath": linkage_r,
        },
        "inputs": {
            "original_task": original_task,
            "draft_output_relpath": draft_out_rel,
            "draft_receipt_relpath": draft_rec_rel,
        },
        "verdict": v,
        "flags": flags,
        "overclaim": {
            "detected": overclaim["detected"],
            "detail": overclaim["detail"],
        },
        "evidence_discipline": ev,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--repo-root", type=Path, default=REPO_ROOT)
    ap.add_argument("--draft-run-id", required=True, help="Run id of the worker draft to review")
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--task", type=str, default=None, help="Original task text (inline)")
    g.add_argument("--task-file", type=Path, help="Path to a file with original task text")
    ap.add_argument(
        "--save",
        action="store_true",
        help="Write JSON to worker_home/peer_reviews/<review_run_id>.json and set linkage in output",
    )
    ap.add_argument(
        "--validate-receipt",
        action="store_true",
        help="Validate draft receipt with jsonschema when installed",
    )
    ap.add_argument("--output", type=Path, default=None, help="Write JSON to this file (default: stdout)")
    args = ap.parse_args()
    root = args.repo_root.resolve()
    if args.task is not None:
        task = args.task
    else:
        tf = args.task_file if args.task_file.is_absolute() else (root / args.task_file)
        task = tf.read_text(encoding="utf-8")

    wh = _worker_home(root)
    review_run_id = _peer_run_id()
    art_rel: str | None = None
    if args.save:
        out_p = wh / "peer_reviews" / f"{review_run_id}.json"
        art_rel = out_p.resolve().relative_to(root).as_posix()
    else:
        out_p = None

    receipt_path = wh / "receipts" / f"{args.draft_run_id}.json"
    if args.validate_receipt:
        rec = json.loads(receipt_path.read_text(encoding="utf-8"))
        _validate(rec, EXECUTION_RECEIPT_SCHEMA_PATH)

    try:
        result = build_peer_review(
            repo_root=root,
            draft_run_id=args.draft_run_id,
            original_task=task,
            review_run_id=review_run_id,
            review_artifact_relpath=art_rel,
        )
    except FileNotFoundError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2

    _validate(result, PEER_SCHEMA_PATH)

    text = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if out_p is not None:
        out_p.parent.mkdir(parents=True, exist_ok=True)
        out_p.write_text(text, encoding="utf-8")
    if args.output is not None:
        outp = args.output if args.output.is_absolute() else (root / args.output)
        outp.parent.mkdir(parents=True, exist_ok=True)
        outp.write_text(text, encoding="utf-8")
    if args.output is None:
        sys.stdout.write(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

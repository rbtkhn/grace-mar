#!/usr/bin/env python3
"""
Atomic integration orchestration for Grace-Mar.

Delegates the real merge to scripts/process_approved_candidates.py (--quick). This script
adds: preflight checks, disk backups of canonical files before merge, optional post-merge
integrity validation, and a JSON receipt under users/<id>/integration-receipts/.

Does not duplicate IX/EVIDENCE/prompt semantics — canonical merge remains process_approved_candidates.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Sequence

REPO_ROOT = Path(__file__).resolve().parent.parent
_SCRIPTS = REPO_ROOT / "scripts"
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from repo_io import assert_canonical_record_layout, profile_dir  # noqa: E402

UTC = timezone.utc
USER_ID_DEFAULT = (os.getenv("GRACE_MAR_USER_ID", "grace-mar").strip() or "grace-mar")
BOT_PROMPT = REPO_ROOT / "bot" / "prompt.py"


def utc_now_iso() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat()


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _prp_path(user_id: str) -> Path:
    if user_id == "grace-mar":
        return REPO_ROOT / "grace-mar-llm.txt"
    return profile_dir(user_id) / f"{user_id}-llm.txt"


def _files_to_backup(user_id: str) -> list[Path]:
    root = profile_dir(user_id)
    paths: list[Path] = [
        root / "self.md",
        root / "self-evidence.md",
        root / "recursion-gate.md",
        BOT_PROMPT,
        root / "self-archive.md",
        root / "merge-receipts.jsonl",
        root / "pipeline-events.jsonl",
        root / "session-log.md",
        _prp_path(user_id),
    ]
    return paths


def _hash_existing(paths: Sequence[Path]) -> dict[str, str]:
    out: dict[str, str] = {}
    for p in paths:
        if p.exists():
            out[str(p.relative_to(REPO_ROOT))] = sha256_text(p.read_text(encoding="utf-8"))
    return out


class AtomicIntegrateError(Exception):
    pass


def _preflight(user_id: str, candidate_id: str, territory: str) -> None:
    assert_canonical_record_layout(user_id, context="atomic_integrate")
    if not BOT_PROMPT.is_file():
        raise AtomicIntegrateError(f"Missing {BOT_PROMPT}")
    # Import merge helpers only after path check
    from process_approved_candidates import _set_user, get_approved_in_candidates  # noqa: E402

    _set_user(user_id)
    approved = get_approved_in_candidates()
    if territory == "wap":
        from recursion_gate_territory import TERRITORY_WAP, territory_from_yaml_block  # noqa: E402

        approved = [c for c in approved if territory_from_yaml_block(c["block"]) == TERRITORY_WAP]
    elif territory == "companion":
        from recursion_gate_territory import TERRITORY_WAP, territory_from_yaml_block  # noqa: E402

        approved = [c for c in approved if territory_from_yaml_block(c["block"]) != TERRITORY_WAP]
    ids = {c["id"] for c in approved}
    if candidate_id not in ids:
        raise AtomicIntegrateError(
            f"{candidate_id} is not an approved candidate in Candidates (territory={territory}). "
            "Approve in the gate first."
        )


def _merge_command(
    user_id: str,
    candidate_id: str,
    approved_by: str,
    territory: str,
) -> list[str]:
    cmd: list[str] = [
        sys.executable,
        str(REPO_ROOT / "scripts" / "process_approved_candidates.py"),
        "-u",
        user_id,
        "--quick",
        candidate_id,
        "--approved-by",
        approved_by,
        "--territory",
        territory,
    ]
    return cmd


def _run_integrity(user_id: str) -> tuple[bool, str]:
    proc = subprocess.run(
        [sys.executable, str(REPO_ROOT / "scripts" / "validate-integrity.py"), "--user", user_id],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
        timeout=120,
    )
    ok = proc.returncode == 0
    msg = ((proc.stdout or "") + "\n" + (proc.stderr or "")).strip()[:4000]
    return ok, msg


@dataclass
class IntegrationReceipt:
    user_id: str
    candidate_id: str
    territory: str
    started_at: str
    completed_at: str | None
    dry_run: bool
    success: bool
    merge_command: list[str]
    merge_returncode: int | None
    merge_stdout: str
    merge_stderr: str
    backup_root_rel: str | None
    before_hashes: dict[str, str]
    after_hashes: dict[str, str]
    integrity_ran: bool
    integrity_ok: bool | None
    integrity_message: str
    error: str | None = None

    def to_json_dict(self) -> dict[str, Any]:
        return asdict(self)


def _write_receipt(user_id: str, receipt: IntegrationReceipt) -> Path:
    root = profile_dir(user_id) / "integration-receipts"
    root.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
    dest = root / f"integration-receipt-{stamp}.json"
    dest.write_text(json.dumps(receipt.to_json_dict(), indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return dest


def _backup_files(paths: Sequence[Path], backup_root: Path) -> None:
    """Copy repo-relative paths under backup_root/<relpath> (mirror layout)."""
    for path in paths:
        if not path.exists():
            continue
        rel = path.relative_to(REPO_ROOT)
        dest = backup_root / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, dest)


def run(
    user_id: str,
    candidate_id: str,
    approved_by: str,
    *,
    apply: bool,
    territory: str,
    skip_integrity: bool,
    merge_runner: Callable[..., subprocess.CompletedProcess[str]] | None = None,
) -> int:
    """
    Run atomic integration. Returns exit code 0 on success, 1 on failure.

    merge_runner: optional subprocess.run replacement for tests.
    """
    runner = merge_runner or subprocess.run
    started = utc_now_iso()
    before_hashes = _hash_existing(_files_to_backup(user_id))
    cmd = _merge_command(user_id, candidate_id, approved_by, territory)

    receipt = IntegrationReceipt(
        user_id=user_id,
        candidate_id=candidate_id,
        territory=territory,
        started_at=started,
        completed_at=None,
        dry_run=not apply,
        success=False,
        merge_command=cmd,
        merge_returncode=None,
        merge_stdout="",
        merge_stderr="",
        backup_root_rel=None,
        before_hashes=before_hashes,
        after_hashes={},
        integrity_ran=False,
        integrity_ok=None,
        integrity_message="",
        error=None,
    )

    try:
        _preflight(user_id, candidate_id, territory)
    except Exception as e:
        receipt.error = str(e)
        receipt.completed_at = utc_now_iso()
        dest = _write_receipt(user_id, receipt)
        print(f"Preflight failed: {e}", file=sys.stderr)
        print(f"Receipt: {dest}", file=sys.stderr)
        return 1

    if not apply:
        receipt.success = True
        receipt.completed_at = utc_now_iso()
        receipt.merge_stdout = "(dry run — merge not executed)"
        dest = _write_receipt(user_id, receipt)
        print(f"Dry run OK. Would run:\n  {' '.join(cmd)}\nReceipt: {dest}")
        return 0

    backup_stamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
    backup_root = profile_dir(user_id) / ".integration-backups" / backup_stamp
    backup_root.mkdir(parents=True, exist_ok=True)
    _backup_files(_files_to_backup(user_id), backup_root)
    receipt.backup_root_rel = str(backup_root.relative_to(REPO_ROOT))

    proc = runner(
        cmd,
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
        timeout=300,
    )
    receipt.merge_returncode = proc.returncode
    receipt.merge_stdout = (proc.stdout or "")[:8000]
    receipt.merge_stderr = (proc.stderr or "")[:8000]

    if proc.returncode != 0:
        receipt.error = f"process_approved_candidates exited {proc.returncode}"
        receipt.completed_at = utc_now_iso()
        dest = _write_receipt(user_id, receipt)
        print(receipt.merge_stderr or receipt.merge_stdout or receipt.error, file=sys.stderr)
        print(f"Receipt: {dest}", file=sys.stderr)
        return 1

    receipt.after_hashes = _hash_existing(_files_to_backup(user_id))

    if not skip_integrity:
        receipt.integrity_ran = True
        ok, msg = _run_integrity(user_id)
        receipt.integrity_ok = ok
        receipt.integrity_message = msg
        if not ok:
            receipt.error = "post-merge validate-integrity.py failed"
            receipt.completed_at = utc_now_iso()
            dest = _write_receipt(user_id, receipt)
            print(msg[:2000], file=sys.stderr)
            print(
                f"Merge subprocess succeeded but integrity check failed. "
                f"Operator restore: compare backup at {receipt.backup_root_rel}",
                file=sys.stderr,
            )
            print(f"Receipt: {dest}", file=sys.stderr)
            return 1

    receipt.success = True
    receipt.completed_at = utc_now_iso()
    dest = _write_receipt(user_id, receipt)
    print(f"Integrated {candidate_id}. Receipt: {dest}")
    return 0


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Orchestrate merge via process_approved_candidates --quick with backups and receipt.",
    )
    p.add_argument("--user-id", "-u", default=USER_ID_DEFAULT, help="Fork id (default GRACE_MAR_USER_ID)")
    p.add_argument("--candidate-id", required=True, help="CANDIDATE-XXXX to merge (must be approved)")
    p.add_argument(
        "--approved-by",
        default=(os.getenv("GRACE_MAR_OPERATOR_NAME", "operator").strip() or "operator"),
        help="Approver name (default GRACE_MAR_OPERATOR_NAME or operator)",
    )
    p.add_argument(
        "--apply",
        action="store_true",
        help="Run merge. Without this flag, preflight only and dry-run receipt.",
    )
    p.add_argument(
        "--territory",
        choices=("all", "wap", "companion"),
        default="all",
        help="Same as process_approved_candidates --territory (default all)",
    )
    p.add_argument(
        "--skip-integrity",
        action="store_true",
        help="Skip validate-integrity.py after successful merge (e.g. CI)",
    )
    return p.parse_args()


def main() -> int:
    args = parse_args()
    cid = args.candidate_id.strip()
    if not cid.upper().startswith("CANDIDATE-"):
        print("candidate-id must look like CANDIDATE-XXXX", file=sys.stderr)
        return 1
    return run(
        args.user_id.strip(),
        cid,
        args.approved_by.strip(),
        apply=bool(args.apply),
        territory=args.territory,
        skip_integrity=bool(args.skip_integrity),
    )


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""
Export a runtime-neutral Grace-Mar bundle.

The bundle separates canonical Record surfaces from runtime continuity and audit:
  - record/
  - policy/
  - runtime/
  - audit/

Usage:
    python scripts/export_runtime_bundle.py -u grace-mar
    python scripts/export_runtime_bundle.py -u grace-mar -o /tmp/runtime-bundle
    python scripts/export_runtime_bundle.py -u grace-mar --mode primary_runtime --include-user-json
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

try:
    from export_fork import export_fork
    from export_intent_snapshot import export_intent_snapshot
    from export_manifest import generate_llms_txt, generate_manifest
    from export_prp import export_prp
    from export_user_identity import export_user_identity, export_user_identity_json
    from harness_events import append_harness_event
    from recursion_gate_review import parse_review_candidates
except ImportError:
    from scripts.export_fork import export_fork
    from scripts.export_intent_snapshot import export_intent_snapshot
    from scripts.export_manifest import generate_llms_txt, generate_manifest
    from scripts.export_prp import export_prp
    from scripts.export_user_identity import export_user_identity, export_user_identity_json
    from scripts.harness_events import append_harness_event
    from scripts.recursion_gate_review import parse_review_candidates


RUNTIME_MODES = {
    "adjunct_runtime": {
        "description": "Assistive runtime alongside the canonical repo.",
        "include_memory": True,
        "include_audit": True,
    },
    "primary_runtime": {
        "description": "Primary live runtime while the repo remains canonical.",
        "include_memory": True,
        "include_audit": True,
    },
    "portable_bundle_only": {
        "description": "Transport bundle without assuming a live runtime session.",
        "include_memory": False,
        "include_audit": True,
    },
}


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _read(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8")


def _write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def _write_json(path: Path, payload: dict | list) -> None:
    _write_text(path, json.dumps(payload, indent=2, ensure_ascii=False) + "\n")


def _sha256_bytes(data: bytes) -> str:
    h = hashlib.sha256()
    h.update(data)
    return h.hexdigest()


def _file_meta(path: Path) -> dict:
    if not path.exists():
        return {"exists": False, "path": str(path)}
    raw = path.read_bytes()
    stat = path.stat()
    return {
        "exists": True,
        "path": str(path),
        "size_bytes": stat.st_size,
        "mtime": datetime.fromtimestamp(stat.st_mtime, tz=timezone.utc).isoformat(),
        "sha256": _sha256_bytes(raw),
    }


def _profile_dir(user_id: str) -> Path:
    return REPO_ROOT / "users" / user_id


def _default_output_dir(user_id: str) -> Path:
    return _profile_dir(user_id) / "runtime-bundle"


def _bundle_id(user_id: str, runtime_mode: str, generated_at: str) -> str:
    digest = _sha256_bytes(f"{user_id}:{runtime_mode}:{generated_at}".encode("utf-8"))
    return digest[:12]


def _warmup_text(user_id: str) -> str:
    profile_dir = _profile_dir(user_id)
    evidence_path = profile_dir / "self-evidence.md"
    session_log_path = profile_dir / "session-log.md"

    pending_ids = [row["id"] for row in parse_review_candidates(user_id) if row.get("status") == "pending"]
    evidence_tail = ""
    if evidence_path.exists():
        lines = [ln for ln in _read(evidence_path).splitlines() if ln.strip()]
        evidence_tail = "\n".join(lines[-12:])
    session_tail = ""
    if session_log_path.exists():
        lines = [ln for ln in _read(session_log_path).splitlines() if ln.strip()]
        session_tail = "\n".join(lines[-12:])
    return (
        "# RUNTIME WARMUP\n\n"
        "> Non-canonical continuity aid. Generated from current repo state.\n\n"
        f"- user_id: `{user_id}`\n"
        f"- pending_candidate_ids: {', '.join(pending_ids) if pending_ids else 'none'}\n\n"
        "## Last evidence tail\n\n"
        f"```\n{evidence_tail or '(none)'}\n```\n\n"
        "## Session-log tail\n\n"
        f"```\n{session_tail or '(none)'}\n```\n"
    )


def _session_log_tail(user_id: str, max_lines: int = 20) -> str:
    session_log_path = _profile_dir(user_id) / "session-log.md"
    lines = [ln for ln in _read(session_log_path).splitlines() if ln.strip()]
    tail = "\n".join(lines[-max_lines:]) if lines else "(none)"
    return (
        "# SESSION-LOG TAIL\n\n"
        "> Non-canonical runtime continuity aid derived from `session-log.md`.\n\n"
        f"```\n{tail}\n```\n"
    )


def _memory_snapshot(user_id: str) -> str:
    memory_path = _profile_dir(user_id) / "memory.md"
    content = _read(memory_path).strip()
    return (
        "# MEMORY SNAPSHOT\n\n"
        "> Non-canonical runtime continuity aid. This is not Record truth.\n\n"
        f"{content or '(memory.md missing or empty)'}\n"
    )


def export_runtime_bundle(
    user_id: str = "grace-mar",
    output_dir: Path | None = None,
    runtime_mode: str = "adjunct_runtime",
    include_user_json: bool = False,
) -> dict:
    if runtime_mode not in RUNTIME_MODES:
        raise ValueError(f"Unknown runtime_mode: {runtime_mode}")

    out_dir = output_dir or _default_output_dir(user_id)
    out_dir.mkdir(parents=True, exist_ok=True)

    record_dir = out_dir / "record"
    policy_dir = out_dir / "policy"
    runtime_dir = out_dir / "runtime"
    audit_dir = out_dir / "audit"
    for lane_dir in (record_dir, policy_dir, runtime_dir, audit_dir):
        lane_dir.mkdir(parents=True, exist_ok=True)

    generated_at = _utc_now_iso()
    bundle_id = _bundle_id(user_id, runtime_mode, generated_at)
    profile_dir = _profile_dir(user_id)

    user_md = export_user_identity(user_id)
    _write_text(record_dir / "USER.md", user_md)
    if include_user_json:
        _write_json(record_dir / "USER.json", export_user_identity_json(user_id))

    _write_json(record_dir / "fork-export.json", export_fork(user_id=user_id, include_raw=True))
    _write_text(record_dir / "grace-mar-llm.txt", export_prp(user_id=user_id))

    manifest = generate_manifest(user_id=user_id, runtime_mode=runtime_mode)
    _write_json(policy_dir / "manifest.json", manifest)
    _write_text(policy_dir / "llms.txt", generate_llms_txt(manifest, user_id))
    intent_snapshot = export_intent_snapshot(user_id)
    _write_json(policy_dir / "intent_snapshot.json", intent_snapshot)

    _write_text(runtime_dir / "warmup.md", _warmup_text(user_id))
    _write_text(runtime_dir / "session-log-tail.md", _session_log_tail(user_id))
    if RUNTIME_MODES[runtime_mode]["include_memory"]:
        _write_text(runtime_dir / "memory.md", _memory_snapshot(user_id))

    audit_sources = [
        "pipeline-events.jsonl",
        "merge-receipts.jsonl",
        "compute-ledger.jsonl",
        "fork-manifest.json",
        "harness-events.jsonl",
    ]
    copied_audit_paths: list[str] = []
    if RUNTIME_MODES[runtime_mode]["include_audit"]:
        for name in audit_sources:
            src = profile_dir / name
            if not src.exists():
                continue
            dst = audit_dir / name
            dst.write_bytes(src.read_bytes())
            copied_audit_paths.append(str(dst.relative_to(out_dir)))

    source_paths = {
        "self": profile_dir / "self.md",
        "skills": profile_dir / "skills.md",
        "evidence": profile_dir / "self-evidence.md",
        "library": profile_dir / "self-library.md",
        "intent": profile_dir / "intent.md",
        "session_log": profile_dir / "session-log.md",
        "memory": profile_dir / "memory.md",
        "prompt": REPO_ROOT / "bot" / "prompt.py",
    }

    derived_paths = [
        record_dir / "USER.md",
        record_dir / "fork-export.json",
        record_dir / "grace-mar-llm.txt",
        policy_dir / "manifest.json",
        policy_dir / "llms.txt",
        policy_dir / "intent_snapshot.json",
        runtime_dir / "warmup.md",
        runtime_dir / "session-log-tail.md",
    ]
    if include_user_json:
        derived_paths.append(record_dir / "USER.json")
    if (runtime_dir / "memory.md").exists():
        derived_paths.append(runtime_dir / "memory.md")
    for rel_path in copied_audit_paths:
        derived_paths.append(out_dir / rel_path)

    bundle_payload = {
        "format": "grace-mar-runtime-bundle",
        "version": "1.0",
        "bundle_id": bundle_id,
        "generated_at": generated_at,
        "user_id": user_id,
        "runtime_mode": runtime_mode,
        "runtime_mode_description": RUNTIME_MODES[runtime_mode]["description"],
        "degraded_mode": (
            {
                "enabled": True,
                "reason": "intent.md missing or invalid; intent_snapshot exported with ok=false",
            }
            if not intent_snapshot.get("ok")
            else {"enabled": False}
        ),
        "lanes": {
            "record": {
                "canonical": True,
                "paths": sorted(str(p.relative_to(out_dir)) for p in record_dir.glob("*") if p.is_file()),
            },
            "policy": {
                "canonical": False,
                "note": "Canonical policy surfaces; not identity truth.",
                "paths": sorted(str(p.relative_to(out_dir)) for p in policy_dir.glob("*") if p.is_file()),
            },
            "runtime": {
                "canonical": False,
                "note": "Continuity aids only. Do not treat as Record truth.",
                "paths": sorted(str(p.relative_to(out_dir)) for p in runtime_dir.glob("*") if p.is_file()),
            },
            "audit": {
                "canonical": False,
                "note": "Append-only replay and provenance surfaces.",
                "paths": copied_audit_paths,
            },
        },
        "canonical_instance_note": (
            "The git-backed Grace-Mar repo remains canonical. This bundle is transport and runtime support, not a new memory authority."
        ),
        "freshness": {
            "source_files": {name: _file_meta(path) for name, path in source_paths.items()},
            "derived_files": {
                str(path.relative_to(out_dir)): _file_meta(path)
                for path in derived_paths
            },
        },
    }
    _write_json(out_dir / "bundle.json", bundle_payload)

    append_harness_event(
        user_id,
        "export_runtime_bundle",
        "runtime_bundle_export",
        path=str(out_dir.resolve()),
        runtime_mode=runtime_mode,
        bundle_id=bundle_id,
        include_user_json=include_user_json,
    )

    return bundle_payload


def main() -> None:
    parser = argparse.ArgumentParser(description="Export a runtime-neutral Grace-Mar bundle")
    parser.add_argument("--user", "-u", default="grace-mar", help="User id")
    parser.add_argument("--output", "-o", default="", help="Output directory (default: users/[id]/runtime-bundle)")
    parser.add_argument(
        "--mode",
        choices=sorted(RUNTIME_MODES.keys()),
        default="adjunct_runtime",
        help="Declared runtime mode",
    )
    parser.add_argument("--include-user-json", action="store_true", help="Write record/USER.json in addition to USER.md")
    args = parser.parse_args()

    out_dir = Path(args.output) if args.output else None
    payload = export_runtime_bundle(
        user_id=args.user,
        output_dir=out_dir,
        runtime_mode=args.mode,
        include_user_json=args.include_user_json,
    )
    print(json.dumps(payload, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()

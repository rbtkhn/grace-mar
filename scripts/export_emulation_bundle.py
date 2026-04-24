#!/usr/bin/env python3
"""
Export an emulation-oriented Grace-Mar bundle by composing existing export surfaces.

This is a thin wrapper over export_runtime_bundle.py plus current policy/review
references. It does not create a second portability stack and it does not grant
foreign runtimes merge authority.
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from datetime import datetime, timezone
from functools import lru_cache
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

try:
    from export_runtime_bundle import RUNTIME_MODES, export_runtime_bundle
    from harness_events import append_harness_event
    from repo_io import profile_dir
except ImportError:
    from scripts.export_runtime_bundle import RUNTIME_MODES, export_runtime_bundle
    from scripts.harness_events import append_harness_event
    from scripts.repo_io import profile_dir

SCHEMA_PATH = REPO_ROOT / "schema-registry" / "emulation-bundle-envelope.v1.json"
CHANGE_PROPOSAL_SCHEMA = REPO_ROOT / "schema-registry" / "change-proposal.v1.json"
AUTHORITY_MAP = REPO_ROOT / "config" / "authority-map.json"
DEFAULT_ADAPTER_EXAMPLES = [
    "bridges/runtime-complements/emulation/README.md",
    "bridges/runtime-complements/emulation/simple_llm_emulation.example.py",
    "bridges/runtime-complements/emulation/langgraph_emulation.example.py",
]
BOUNDARY_NOTICE = (
    "This emulation bundle is a governed loading package over existing Grace-Mar exports. "
    "Foreign runtimes may emulate behavior, hold runtime-only notes, and emit proposals or "
    "runtime observations, but they may not write canonical Record files directly or bypass "
    "the Sovereign Merge Rule."
)


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _default_output_dir(user_id: str) -> Path:
    return profile_dir(user_id) / "emulation-bundle"


def _write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def _copy_json(src: Path, dst: Path) -> None:
    payload = json.loads(src.read_text(encoding="utf-8"))
    _write_json(dst, payload)


@lru_cache(maxsize=1)
def _emulation_envelope_validator():
    try:
        import jsonschema
    except ImportError as exc:
        raise RuntimeError(
            "jsonschema is required to validate emulation bundle exports"
        ) from exc

    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    jsonschema.validators.validator_for(schema).check_schema(schema)
    return jsonschema.Draft202012Validator(schema)


def validate_emulation_envelope(payload: dict) -> None:
    _emulation_envelope_validator().validate(payload)


def build_emulation_envelope(
    *,
    user_id: str,
    runtime_mode: str,
    generated_at: str,
    adapter_examples: list[str] | None = None,
) -> dict:
    examples = adapter_examples if adapter_examples is not None else list(DEFAULT_ADAPTER_EXAMPLES)
    return {
        "$schema": "schema-registry/emulation-bundle-envelope.v1.json",
        "schemaVersion": "1.0.0",
        "format": "grace-mar-emulation-bundle",
        "generatedAt": generated_at,
        "userId": user_id,
        "runtimeMode": runtime_mode,
        "runtimeBundlePath": "bundle.json",
        "references": {
            "prpPath": "record/grace-mar-llm.txt",
            "forkExportPath": "record/fork-export.json",
            "authorityMapPath": "policy/authority-map.json",
            "changeProposalSchemaPath": "policy/change-proposal.v1.json",
        },
        "boundaryNotice": BOUNDARY_NOTICE,
        "proposalReturn": {
            "schemaPath": "policy/change-proposal.v1.json",
            "humanReviewRequired": True,
            "canonicalSurfacesTouched": False,
            "notes": (
                "Durable changes should return as change-proposal objects or equivalent reviewed "
                "drafts, then move through existing gate/review paths."
            ),
        },
        "runtimeObservationReturn": {
            "importScript": "scripts/runtime/import_runtime_observation.py",
            "humanReviewRequired": True,
            "canonicalSurfacesTouched": False,
            "notes": (
                "Runtime-only observations should enter through the runtime-complements membrane "
                "and remain non-canonical until a human explicitly stages them further."
            ),
        },
        "adapterExamples": examples,
    }


def export_emulation_bundle(
    *,
    user_id: str = "grace-mar",
    output_dir: Path | None = None,
    runtime_mode: str = "portable_bundle_only",
    include_user_json: bool = False,
) -> dict:
    if runtime_mode not in RUNTIME_MODES:
        raise ValueError(f"Unknown runtime mode: {runtime_mode}")

    t0 = time.monotonic()
    out_dir = output_dir or _default_output_dir(user_id)
    out_dir.mkdir(parents=True, exist_ok=True)

    export_runtime_bundle(
        user_id=user_id,
        output_dir=out_dir,
        runtime_mode=runtime_mode,
        include_user_json=include_user_json,
    )

    policy_dir = out_dir / "policy"
    _copy_json(AUTHORITY_MAP, policy_dir / "authority-map.json")
    _copy_json(CHANGE_PROPOSAL_SCHEMA, policy_dir / "change-proposal.v1.json")

    envelope = build_emulation_envelope(
        user_id=user_id,
        runtime_mode=runtime_mode,
        generated_at=_utc_now_iso(),
    )
    validate_emulation_envelope(envelope)
    _write_json(out_dir / "emulation-bundle.json", envelope)

    append_harness_event(
        user_id,
        "export_emulation_bundle",
        "emulation_bundle_export",
        path=str(out_dir.resolve()),
        runtime_mode=runtime_mode,
        include_user_json=include_user_json,
    )

    wall_ms = int((time.monotonic() - t0) * 1000)
    try:
        if str(REPO_ROOT / "scripts") not in sys.path:
            sys.path.insert(0, str(REPO_ROOT / "scripts"))
        from emit_compute_ledger import append_integration_ledger

        total_bytes = 0
        for path in out_dir.rglob("*"):
            if path.is_file():
                try:
                    total_bytes += path.stat().st_size
                except OSError:
                    pass
        append_integration_ledger(
            user_id,
            operation="emulation_bundle_export",
            runtime="export_emulation_bundle",
            success=True,
            wall_ms=wall_ms,
            bytes_processed=total_bytes,
            source_artifact_count=sum(1 for _ in out_dir.rglob("*") if _.is_file()),
            task_type="export",
            repo_root=REPO_ROOT,
        )
    except Exception:
        pass

    return envelope


def main() -> None:
    parser = argparse.ArgumentParser(description="Export an emulation-oriented Grace-Mar bundle")
    parser.add_argument("--user", "-u", default="grace-mar", help="User id")
    parser.add_argument(
        "--output",
        "-o",
        default="",
        help="Output directory (default: users/[id]/emulation-bundle)",
    )
    parser.add_argument(
        "--mode",
        choices=sorted(RUNTIME_MODES.keys()),
        default="portable_bundle_only",
        help="Declared runtime mode for the underlying runtime bundle",
    )
    parser.add_argument(
        "--include-user-json",
        action="store_true",
        help="Write record/USER.json in addition to USER.md",
    )
    args = parser.parse_args()

    out_dir = Path(args.output) if args.output else None
    payload = export_emulation_bundle(
        user_id=args.user,
        output_dir=out_dir,
        runtime_mode=args.mode,
        include_user_json=args.include_user_json,
    )
    print(json.dumps(payload, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()

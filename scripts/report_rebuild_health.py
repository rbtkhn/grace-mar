#!/usr/bin/env python3
"""Summarize repo-owned derived rebuild health from receipts."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_RECEIPTS_DIR = REPO_ROOT / "artifacts" / "work-dev" / "rebuild-receipts"
DEFAULT_OUTPUT = REPO_ROOT / "artifacts" / "work-dev" / "rebuild-health" / "summary.json"
DEFAULT_MANIFEST = REPO_ROOT / "artifacts" / "work-dev" / "derived-regeneration-manifest.json"


def _load_receipts(directory: Path) -> list[dict]:
    rows: list[dict] = []
    if not directory.is_dir():
        return rows
    for path in sorted(directory.glob("*.json")):
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            continue
        if isinstance(payload, dict) and payload.get("receiptKind") == "derived_rebuild":
            rows.append(payload)
    return rows


def _load_manifest(path: Path) -> dict | None:
    if not path.is_file():
        return None
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return None
    return payload if isinstance(payload, dict) else None


def build_health_payload(receipts: list[dict], manifest: dict | None) -> dict:
    target_counter: Counter[str] = Counter()
    result_counter: Counter[str] = Counter()
    total_elapsed_ms = 0
    total_target_runs = 0
    newest_created_at = None

    for receipt in receipts:
        result_counter[str(receipt.get("resultStatus") or "unknown")] += 1
        created_at = receipt.get("createdAt")
        if isinstance(created_at, str) and created_at:
            if newest_created_at is None or created_at > newest_created_at:
                newest_created_at = created_at
        for target in receipt.get("targets", []):
            if not isinstance(target, dict):
                continue
            target_id = str(target.get("targetId") or "unknown")
            target_counter[target_id] += 1
            total_target_runs += 1
            elapsed_ms = target.get("elapsedMs")
            if isinstance(elapsed_ms, int):
                total_elapsed_ms += elapsed_ms

    manifest_target_count = 0
    if manifest and isinstance(manifest.get("targets"), list):
        manifest_target_count = len(manifest["targets"])

    avg_elapsed_ms = 0
    if total_target_runs:
        avg_elapsed_ms = int(total_elapsed_ms / total_target_runs)

    return {
        "schemaVersion": "1.0.0-rebuild-health",
        "generatedAt": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "recordAuthority": "none",
        "gateEffect": "none",
        "receiptCount": len(receipts),
        "latestReceiptAt": newest_created_at,
        "manifestTargetCount": manifest_target_count,
        "resultStatusCounts": dict(result_counter),
        "topTargets": [
            {"targetId": target_id, "runs": count}
            for target_id, count in target_counter.most_common(10)
        ],
        "avgTargetElapsedMs": avg_elapsed_ms,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--receipts-dir",
        type=Path,
        default=DEFAULT_RECEIPTS_DIR,
        help="directory containing derived rebuild receipts",
    )
    parser.add_argument(
        "--manifest",
        type=Path,
        default=DEFAULT_MANIFEST,
        help="derived regeneration manifest path",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help="output summary JSON path",
    )
    args = parser.parse_args()

    receipts_dir = args.receipts_dir if args.receipts_dir.is_absolute() else (REPO_ROOT / args.receipts_dir).resolve()
    manifest_path = args.manifest if args.manifest.is_absolute() else (REPO_ROOT / args.manifest).resolve()
    out = args.output if args.output.is_absolute() else (REPO_ROOT / args.output).resolve()

    payload = build_health_payload(_load_receipts(receipts_dir), _load_manifest(manifest_path))
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

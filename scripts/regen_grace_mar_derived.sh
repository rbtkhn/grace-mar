#!/usr/bin/env bash
# Refresh grace-mar derived exports and runtime bundle (integrity: stale derived export).
# Run from repo root after profile/prompt changes, or when validate-integrity reports stale mtimes.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
python3 scripts/export_manifest.py -u grace-mar
python3 scripts/fork_checksum.py -u grace-mar --manifest
python3 scripts/export_prp.py -u grace-mar -o grace-mar-llm.txt
python3 scripts/export_runtime_bundle.py -u grace-mar
echo "Done. Verify: python3 scripts/validate-integrity.py --user grace-mar --json" >&2

#!/usr/bin/env bash
# Operator merge ritual: validate-integrity → merge command → validate-integrity.
#
# Usage:
#   GRACE_MAR_USER_ID=grace-mar ./scripts/operator_merge_once.sh -- python3 scripts/atomic_integrate.py -u grace-mar --candidate-id CANDIDATE-XXXX --approved-by <name> --apply --skip-integrity
#   GRACE_MAR_USER_ID=grace-mar ./scripts/operator_merge_once.sh -- python3 scripts/process_approved_candidates.py -u grace-mar --apply --approved-by <name> --receipt /tmp/r.json
#
# Use --skip-integrity with atomic_integrate here so the merge step does not duplicate the
# postflight validate-integrity (this script runs integrity before and after the merge).
#
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO_ROOT"

PYTHON="${PYTHON:-python3}"
USER_ID="${GRACE_MAR_USER_ID:-grace-mar}"

help() {
  echo "Usage: GRACE_MAR_USER_ID=<id> $0 -- <merge command...>" >&2
  echo "  Runs: validate-integrity.py --user \$USER_ID  →  \$@  →  validate-integrity.py again" >&2
  echo "Example:" >&2
  echo "  $0 -- $PYTHON scripts/atomic_integrate.py -u grace-mar --candidate-id CANDIDATE-0001 --approved-by operator --apply --skip-integrity" >&2
}

if [[ "${1:-}" == "-h" ]] || [[ "${1:-}" == "--help" ]]; then
  help
  exit 0
fi

if [[ $# -lt 1 ]]; then
  help
  exit 1
fi
if [[ "${1:-}" != "--" ]]; then
  echo "Error: use -- before the merge command (see --help)" >&2
  help
  exit 1
fi
shift
if [[ $# -lt 1 ]]; then
  help
  exit 1
fi

echo "==> operator_merge_once: preflight validate-integrity ($USER_ID)"
"$PYTHON" scripts/validate-integrity.py --user "$USER_ID"

echo "==> operator_merge_once: merge step"
"$@"

echo "==> operator_merge_once: postflight validate-integrity ($USER_ID)"
"$PYTHON" scripts/validate-integrity.py --user "$USER_ID"

echo "operator_merge_once: OK"

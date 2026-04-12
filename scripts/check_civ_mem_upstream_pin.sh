#!/usr/bin/env bash
# Compare local civilization_memory HEAD to docs/ci/civilization_memory_upstream.env pin.
# Exit 0: match or no checkout (informational skip). Exit 1: mismatch.
# Usage: bash scripts/check_civ_mem_upstream_pin.sh

set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
ENV_FILE="${ROOT}/docs/ci/civilization_memory_upstream.env"
REPO="${ROOT}/research/repos/civilization_memory"

if [[ ! -f "${ENV_FILE}" ]]; then
  echo "error: missing ${ENV_FILE}" >&2
  exit 2
fi

PIN_LINE="$(grep -E '^CIV_MEM_UPSTREAM_SHA=' "${ENV_FILE}" | head -1 || true)"
PIN="${PIN_LINE#CIV_MEM_UPSTREAM_SHA=}"
PIN="$(echo "${PIN}" | tr -d '\r' | tr -d ' ')"

if [[ ! -d "${REPO}/.git" ]]; then
  echo "civ-mem pin check: no checkout at research/repos/civilization_memory — skip (CI still uses pin in ${ENV_FILE})"
  exit 0
fi

HEAD="$(git -C "${REPO}" rev-parse HEAD 2>/dev/null || echo "")"
if [[ -z "${HEAD}" ]]; then
  echo "civ-mem pin check: could not read HEAD in ${REPO}" >&2
  exit 2
fi

if [[ "${HEAD}" == "${PIN}" ]]; then
  echo "civ-mem pin check: OK (matches docs/ci pin ${PIN:0:12}…)"
  exit 0
fi

echo "civ-mem pin check: MISMATCH — local HEAD ${HEAD}" >&2
echo "  expected pin: ${PIN} (from docs/ci/civilization_memory_upstream.env)" >&2
echo "  run: scripts/ci/clone_civilization_memory.sh  or  git -C ${REPO} fetch && git -C ${REPO} checkout ${PIN}" >&2
exit 1

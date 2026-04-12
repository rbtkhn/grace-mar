#!/usr/bin/env bash
# Clone upstream civilization_memory at the pinned commit (see docs/ci/civilization_memory_upstream.env).
# Used by GitHub Actions; safe to run locally into research/repos/civilization_memory.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$ROOT"

PIN="${ROOT}/docs/ci/civilization_memory_upstream.env"
if [[ ! -f "$PIN" ]]; then
  echo "clone_civilization_memory.sh: missing ${PIN}" >&2
  exit 1
fi

set -a
# shellcheck disable=SC1090
source "$PIN"
set +a

: "${CIV_MEM_UPSTREAM_URL:?set in docs/ci/civilization_memory_upstream.env}"
: "${CIV_MEM_UPSTREAM_SHA:?set in docs/ci/civilization_memory_upstream.env}"

TARGET="${ROOT}/research/repos/civilization_memory"
rm -rf "$TARGET"
mkdir -p "$(dirname "$TARGET")"

git init "$TARGET"
cd "$TARGET"
git remote add origin "$CIV_MEM_UPSTREAM_URL"
git fetch --depth 1 origin "$CIV_MEM_UPSTREAM_SHA"
git checkout FETCH_HEAD

echo "civilization_memory pinned at $(git rev-parse HEAD)"

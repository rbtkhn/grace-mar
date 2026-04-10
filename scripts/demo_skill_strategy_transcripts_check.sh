#!/usr/bin/env bash
# Read-only: verify the three 2026-04-10 skill-strategy demo transcript digests exist.
# Usage: from repo root — bash scripts/demo_skill_strategy_transcripts_check.sh
# Exit 0 if all present; exit 1 if any missing.

set -euo pipefail
REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"

FILES=(
  "research/external/work-strategy/transcripts/2026-04-10-diesen-mearsheimer-iran-ceasefire-truth-social.md"
  "research/external/work-strategy/transcripts/mercouris-2026-04-10-good-friday-hormuz-lebanon-islamabad.md"
  "research/external/work-strategy/transcripts/2026-04-10-davis-crooke-centcom-iran-hormuz-islamabad.md"
)

MISSING=0
for f in "${FILES[@]}"; do
  if [[ ! -f "$REPO_ROOT/$f" ]]; then
    echo "MISSING: $f" >&2
    MISSING=1
  else
    echo "OK: $f"
  fi
done

if [[ "$MISSING" -ne 0 ]]; then
  echo "demo_skill_strategy_transcripts_check: failed (missing files)." >&2
  exit 1
fi

echo "All digest files present."
exit 0

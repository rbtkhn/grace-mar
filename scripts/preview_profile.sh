#!/usr/bin/env bash
# Generate profile and open it in the default browser (fast local loop).
set -e
cd "$(dirname "$0")/.."
python3 scripts/generate_profile.py
if command -v open >/dev/null 2>&1; then
  open profile/index.html
elif command -v xdg-open >/dev/null 2>&1; then
  xdg-open profile/index.html
else
  echo "Profile generated at profile/index.html — open it in your browser."
fi

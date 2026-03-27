#!/usr/bin/env bash
# Append one continuity read log line, then run the rest of the command (e.g. OpenClaw).
# Usage: scripts/openclaw_session_continuity.sh <command> [args...]
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
USER_ID="${GRACE_MAR_USER_ID:-grace-mar}"
python3 "$ROOT/scripts/continuity_read_log.py" -u "$USER_ID"
exec "$@"

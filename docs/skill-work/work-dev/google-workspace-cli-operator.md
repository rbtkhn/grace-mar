# Google Workspace CLI (operator-only)

**Scope:** Optional **operator** tooling for Sheets/Drive append-only continuity — **not** Voice knowledge, **not** the Record, **not** a substitute for git or RECURSION-GATE.

**Prereq:** Install [`@googleworkspace/cli`](https://www.npmjs.com/package/@googleworkspace/cli) and complete OAuth in a dedicated GCP project. Never commit refresh tokens, client secrets, or `.env` files with credentials.

## Local config (git-safe)

- Repo `.gitignore` already ignores `.env.*.local`. Use e.g. `.env.gws.local` in the repo root:

  ```bash
  # Example keys only — create the file locally; do not commit.
  export GWS_SPREADSHEET_ID="your_sheet_id"
  export GWS_AUDIT_SHEET_ID="optional_second_sheet"
  export GWS_EVIDENCE_FOLDER_ID="optional_drive_folder"
  ```

- Before running recipes: `set -a && source .env.gws.local && set +a` (bash/zsh).

## Where to log `gws` runs

- **Do not** append operator tooling notes to `users/grace-mar/session-log.md` (that file is interaction / session history for the instance).
- Prefer a **local, untracked** log under work-dev, e.g. create `docs/skill-work/work-dev/operator-gws-log.local.md` on your machine and add that basename to your **personal** git exclude if needed.
- Log: timestamp, command shape (not secrets), spreadsheet ID redacted or last 4 chars, and outcome.

## Recipes (build timestamps in the shell)

Shell-JSON is easy to get wrong: compute `TS` and row values in the shell, then pass JSON.

### A — Append heartbeat row

```bash
TS=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
# After: source .env.gws.local with GWS_SPREADSHEET_ID set
python3 -c "
import json, os, sys
row = [[
  sys.argv[1],
  'reentry',
  'active_thread=…',
  'commit=' + sys.argv[2],
  'territories=…',
  'notes=…',
]]
print(json.dumps({'values': row}))
" "$TS" "$(git rev-parse --short HEAD)" > /tmp/gws_row.json

gws sheets spreadsheets values append \
  --params "{\"spreadsheetId\":\"${GWS_SPREADSHEET_ID}\",\"range\":\"Heartbeat Log!A:F\",\"valueInputOption\":\"RAW\"}" \
  --json "$(cat /tmp/gws_row.json)"
```

Adjust sheet name `Heartbeat Log` to match your tab.

### B — Append audit row

Same pattern as A; use `GWS_AUDIT_SHEET_ID` and a range like `Audit!A:E`.

### C — Read-only Drive list (safest first step)

Use a **current** ISO date lower bound (e.g. this year):

```bash
YEAR=$(date +%Y)
gws drive files list \
  --params "{\"q\":\"'${GWS_EVIDENCE_FOLDER_ID}' in parents and modifiedTime > '${YEAR}-01-01T00:00:00Z'\",\"pageSize\":10,\"orderBy\":\"modifiedTime desc\"}" \
  --json
```

## Guardrails

- Prefer `--json` for machine-shaped output.
- Start with **read-only** commands until the operator confirms the project and scopes.
- Never paste OAuth secrets into chat or commit them.

**Cursor:** Attach `.cursor/rules/gws-cli-recipes.mdc` when working from this doc so the model has the short pointer without loading OAuth detail on every thread.

# Operator Console

**Purpose:** Parent/operator UX that removes markdown from the critical path. Submit observations, upload artifacts, review staged candidates, and inspect the fork timeline without editing repo files directly. Governance and exportability are unchanged; the console uses the same gate and pipeline.

---

## What it is

A single browser page (served by the Mini App server) with four tabs:

| Tab | Purpose |
|-----|--------|
| **Observe** | Submit an observation (same pipeline as saying "we did X" in Telegram). Text is sent to the analyst; any staged candidate appears in the Gate tab. No need to open or edit `recursion-gate.md`. |
| **Upload** | Upload a file to `users/<id>/artifacts/` and optionally add a note. The note is submitted as an observation so the analyst can stage a candidate linking the artifact. |
| **Gate** | View pending candidates; Approve / Reject / Quick merge. After approval, **Merge approved (companion)** / **(all)** / **(work-politics territory only)** runs `process_approved_candidates` on the server — same as the CLI receipt flow, without pasting commands. |
| **Timeline** | Read-only view of recent pipeline events (staged, applied, etc.) from `pipeline-events.jsonl`. Fork history at a glance without opening markdown. |

---

## How to use

1. **Run the server** (e.g. `python apps/miniapp_server.py` or your deployed Mini App URL).
2. **Open the console:** `/operator/console` (e.g. `https://your-host/operator/console`).
3. **Enter the operator secret** (same as `OPERATOR_FETCH_SECRET`). You can bookmark with `?token=...` or use Save to store it in the browser.
4. Use **Observe** to add observations, **Upload** for artifacts, **Gate** to review and approve/reject, **Timeline** to see recent activity.

Gate actions and **Merge approved** go through the same APIs as the CLI. Merges write `self.md`, `self-evidence.md`, `recursion-gate.md`, prompt, PRP export, etc. **Hosting:** merge-from-browser only works if `apps/miniapp_server.py` runs with a **writable git checkout** of the repo (many PaaS disks are ephemeral or read-only — use a persistent volume or run merge from a machine with the repo). Approve/reject alone only edit `recursion-gate.md`.

---

## API (for the console)

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/operator/observations` | POST | Submit observation text → analyst → stage to gate |
| `/operator/artifacts` | POST | Upload file + optional observation → save to artifacts, stage if signal |
| `/operator/gate-candidates` | GET | List candidates (filter by status, etc.) |
| `/operator/gate-candidates/<id>/action` | POST | approve / reject / defer / quick_merge |
| `/operator/gate-candidates/merge-approved` | POST | Body `{"territory":"companion"|"wap"|"all"}`. Batch-merge all **approved** candidates in that slice (default `companion` = non–work-politics territory). Runs `process_approved_candidates --apply` with a server-generated receipt. |
| `/operator/timeline` | GET | Recent pipeline events (read-only) |

Authentication: `Authorization: Bearer <OPERATOR_FETCH_SECRET>` (or `OPERATOR_SECRET` where used).

---

## Relation to other surfaces

- **Telegram** — "We did X", `/review`, approve/reject: same pipeline. Console is another way to submit and review without opening files.
- **Approval Inbox** (`/operator/inbox`) — Richer gate UI (filters, batch, receipt download). Same **Merge approved** buttons as the Console Gate tab.
- **CLI** — `process_approved_candidates.py`, `operator_gate_snapshot.py`, etc. still apply. Console does not replace them; it adds a browser path that avoids markdown for day-to-day use.

---

## For families

The console makes the system usable for operators who are not comfortable editing markdown or running scripts. They can log in once, save the secret, then submit what happened, upload homework or art, and approve what should go into the Record — all from the browser. The underlying governance (one gate, companion approval, audit in pipeline-events) is preserved.

# work-politics internal dashboard (SMM + operator)

**Purpose:** Internal web surface for **work-politics** — you and the social media manager track **jobs** (news scan, X drafts, brief hooks) without losing work when a Cursor thread closes. **Not** a client portal in v1; **not** autonomous posting or LLM-on-server (unless added later).

**URL (when deployed):** `https://<miniapp-host>/pol` (legacy **`/wap`** still works)  
**Auth:** `POL_DASHBOARD_TOKEN` (or legacy `WAP_DASHBOARD_TOKEN`) — send as `X-Pol-Token` / `X-Wap-Token` or `Authorization: Bearer <token>`, or bookmark `https://<host>/pol?t=<token>`.

---

## Environment

| Variable | Required | Description |
|----------|----------|-------------|
| `POL_DASHBOARD_TOKEN` | Yes (to use dashboard) | Preferred. Long random secret. Share only with operator + SMM. |
| `WAP_DASHBOARD_TOKEN` | Legacy | Still read if `POL_DASHBOARD_TOKEN` is unset. |
| `POL_JOBS_PATH` | No | Preferred path to jobs JSON (absolute or repo-relative). |
| `WAP_JOBS_PATH` | Legacy | Used if `POL_JOBS_PATH` unset. Default file: `data/wap_jobs.json` under repo root. On Render, use a **persistent disk** mount path if you need jobs to survive redeploys; otherwise data is ephemeral like session-transcript. |

**Do not** paste API keys, passwords, or campaign secrets into job **context** or **output** fields if the jobs file might be copied or committed. Treat stored text as **operational notes** only.

---

## SMM daily workflow

1. Open `/pol` with token; create a **new job** (client, workflow type, context, optional URLs).
2. In Cursor, run the matching skill (e.g. `.cursor/skills/massie-x-news-search-draft/SKILL.md`) with that context.
3. Paste agent output into the job; set status **output_pasted**.
4. Edit and post from X (@usa_first_ky); set status **shipped** when done.
5. Keep [content-queue.md](skill-work/work-politics/content-queue.md) in sync for content state (idea → posted).

---

## API (token required)

| Method | Path | Body / query |
|--------|------|----------------|
| GET | `/api/pol/jobs` (legacy `/api/wap/jobs`) | `?limit=100` — list jobs, newest first |
| POST | `/api/pol/jobs` | JSON: `client_slug`, `workflow`, `context`, `urls` (optional) |
| PATCH | `/api/pol/jobs/<id>` | JSON: any of `status`, `output`, `context`, `urls` |

Statuses: `new` → `ran_in_cursor` → `output_pasted` → `shipped`.

---

## Phase 2 (not implemented)

- Per-client tokens, read-only history for campaigns, approve-draft audit log.
- Optional server-side LLM calls (keys, cost, compliance).

---

## Related

- [consulting-charter.md](skill-work/work-politics/consulting-charter.md) — human approves public ship.
- [miniapp-setup.md](miniapp-setup.md) — deploy and env vars.
- [smm-workspace.md](skill-work/work-politics/smm-workspace.md) — SMM entry point.

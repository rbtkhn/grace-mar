# Telegram Mini App Setup

**Channel roles:**
- **HTML profile** — Read-only. View identity, pipeline, SKILLS, benchmarks. No input, no chat.
- **Telegram** — Bidirectional. User and Grace-Mar exchange messages; "we did X" invokes the pipeline. The primary conversation channel.

Grace-Mar has several web surfaces on the Mini App host (plus the static dashboard):

- **Dashboard** — Full profile view (Knowledge, Skills, Curiosity, Personality, Library, Disclosure). **Browser only, read-only.** Available at **https://grace-mar.com**.
- **Q&A Mini App** — Interactive Q&A with Grace-Mar. Runs as a **Telegram Mini App** and can also be opened in a browser. Bidirectional (ask questions, get answers).
- **Family hub** — `/app` on the Mini App server: chat, log activities (“we did X”), and parent-gated review + merge. See below.
- **WAP internal dashboard** — `/wap`: token-gated job tracker for work-politics (SMM + operator). See [wap-dashboard.md](wap-dashboard.md).

## Architecture

| Surface | Host | URL | Purpose |
|---------|------|-----|---------|
| Dashboard (HTML) | grace-mar.com | **https://grace-mar.com** | Read-only — view profile, pipeline, SKILLS, disclosure |
| Q&A Mini App | Render / Railway / your host | e.g. `https://grace-mar.onrender.com/` | Bidirectional — ask Grace-Mar questions, see her voice |

The **profile** is at **https://grace-mar.com**. Set `PROFILE_MINIAPP_URL` (or `DASHBOARD_MINIAPP_URL`) to **https://grace-mar.com** so the Telegram menu button opens the profile. (If you prefer the menu button to open the Q&A Mini App instead, set it to that URL.)

## 1. Dashboard (browser-only, read-only)

The profile is available at **https://grace-mar.com**. Generate the static HTML with `scripts/generate_profile.py`; deploy via GitHub Pages (point grace-mar.com at the Pages site) or serve from your own host. **Full steps:** [profile-deploy.md](profile-deploy.md).

Generate and deploy:

```bash
python3 scripts/generate_profile.py
```

Push to `main` or run the workflow manually. `.github/workflows/pages.yml` generates the profile and deploys `profile/` to the `gh-pages` branch. Enable GitHub Pages in the repo (Settings → Pages → Source: Deploy from branch → branch: `gh-pages`, folder: `/ (root)`). Point **grace-mar.com** at the Pages site (Settings → Pages → Custom domain) so the profile lives at https://grace-mar.com.

## 2. Q&A Mini App (Mini App + API)

The Q&A app consists of:

- Static UI: `miniapp/index.html`
- API: `POST /api/ask` with `{ "message": "..." }` → `{ "response": "..." }`
- Server: `miniapp_server.py` serves both

### Run locally

```bash
pip install -r requirements.txt
OPENAI_API_KEY=sk-... python miniapp_server.py
```

Open http://localhost:5000 for the Q&A Mini App. For the **family hub**, set `FAMILY_APP_TOKEN` in `.env`, restart, then open http://localhost:5000/app and paste the token (or use `/app?t=<token>` once).

For Telegram testing, expose with ngrok:

```bash
ngrok http 5000
```

### Deploy (Railway / Render)

**Railway**

1. Connect the repo.
2. Root directory = repo root. Railway uses `procfile` and `requirements.txt`.
3. Set env: `OPENAI_API_KEY`, `PORT` (optional, Railway sets it).
4. Deploy. Use the generated URL (e.g. `https://grace-mar-qa.railway.app`).

**Render**

- **Option A — Blueprint:** Add `render.yaml` to your repo. In Render Dashboard → New → Blueprint, connect the repo. Both the Mini App (web) and the bot (worker) will be created. Set env vars in each service’s Environment tab.
- **Option B — Manual:** New Web Service, connect repo. Build: `pip install -r requirements.txt`. Start: `python miniapp_server.py`. Set `OPENAI_API_KEY`, and optionally `GITHUB_TOKEN`, `GRACE_MAR_REPO`.

### Archive (session transcript)

Mini App exchanges are appended to `users/<user>/session-transcript.md` (real-time log, same policy as Telegram). SELF-ARCHIVE is updated only when candidates are merged via `process_approved_candidates` (gated). No GitHub token is required for archiving.

On Render, the filesystem is ephemeral, so SESSION-TRANSCRIPT written by the Mini App is lost between deploys unless you add a separate step to persist it (e.g. push to repo). Local dev writes to disk as usual.

**Operator Console — merge from browser:** Gate tab and Inbox can run **Merge approved (companion)** / **(all)** / **(WAP)**, which invokes `process_approved_candidates` on the server. That requires a **writable clone** of the repo; ephemeral-only hosts may fail merges. Use the CLI from your laptop, or attach a persistent disk, if web merge errors out.

### Family hub (`/app`)

**Env:** Set **`FAMILY_APP_TOKEN`** to a long random string (same host as `miniapp_server.py`). Optional bookmark: `https://<host>/app?t=<FAMILY_APP_TOKEN>` — the app stores the token in the browser after the first load.

**APIs (require header `X-Family-Token: <FAMILY_APP_TOKEN>`):**

| Endpoint | Purpose |
|----------|---------|
| `POST /api/family/activity` | Body `{ "text": "we read …" }` — stages like Telegram “we did X” (`channel_key`: `web:family`). |
| `GET /api/family/pending-count` | Pending candidate count (for badges). |
| `POST /api/family/ask` | Same shape as `POST /api/ask` — Voice chat; archives to session-transcript. |

**Review tab:** Parent enters **`OPERATOR_FETCH_SECRET`** once per browser session; then uses the same gate + merge-approved flow as [Operator Console](operator-console.md). Kids do not need the operator secret for Chat or Log.

**Security:** Anyone with `FAMILY_APP_TOKEN` can chat and submit activities (rate-limit at reverse proxy if needed). Rotate the token if the link leaks. Merge still requires the operator secret.

### WAP internal dashboard (`/wap`)

**Env:** Set **`WAP_DASHBOARD_TOKEN`** to a long random string. Optional **`WAP_JOBS_PATH`** — absolute path or path relative to repo root for the jobs JSON file (default `data/wap_jobs.json`). On Render, jobs are **ephemeral** unless you mount a persistent disk and point `WAP_JOBS_PATH` there.

**Use:** Open `https://<host>/wap?t=<WAP_DASHBOARD_TOKEN>` (token is stored in the browser session). Create jobs, paste Cursor outputs, update status. **Full spec:** [wap-dashboard.md](wap-dashboard.md).

## 3. Bot (Webhook Mode)

The `render.yaml` blueprint runs the Telegram bot via **webhook** on the miniapp service (no separate worker). Set these env vars on the **miniapp** service:

- `TELEGRAM_BOT_TOKEN` — from @BotFather (when set, webhook is enabled)
- `OPENAI_API_KEY`
- `PROFILE_MINIAPP_URL` — URL opened by the Telegram menu button (e.g. **https://grace-mar.com** for the profile); `DASHBOARD_MINIAPP_URL` still supported
- Session transcript is written locally; SELF-ARCHIVE is updated only on merge (no GITHUB_TOKEN needed for archiving).

See [TELEGRAM-WEBHOOK-SETUP](telegram-webhook-setup.md) for details and migration from polling.

## 4. Bot env (local)

When running the bot locally, set in `bot/.env`:

```env
PROFILE_MINIAPP_URL=https://grace-mar.com
# or DASHBOARD_MINIAPP_URL=https://grace-mar.com
# Optional: base URL for Operator Console hints after Telegram approve (/merge)
# GRACE_MAR_OPERATOR_CONSOLE_URL=https://your-miniapp-host.example.com
```

This URL is opened when the user taps the Telegram menu button (Profile). Set it to **https://grace-mar.com** so the profile is one tap away. On Render, set the same var in the bot service’s Environment tab.

## 5. @BotFather (optional)

In @BotFather → Bot Settings → Menu Button:

- Set URL to **https://grace-mar.com** (or whatever URL you set in `PROFILE_MINIAPP_URL` or `DASHBOARD_MINIAPP_URL`).

## 6. Deep linking

Use `startapp` to open the Q&A app:

- `t.me/your_bot?startapp=` — opens the Q&A Mini App.

## Security

- The Q&A API is stateless and uses the same `SYSTEM_PROMPT` as the bot. No profile writes from the Mini App.
- For production, consider rate limiting and `initData` validation (HMAC-SHA-256 with bot token) if you need user verification.

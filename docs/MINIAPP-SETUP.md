# Telegram Mini App Setup

Grace-Mar has two web surfaces:

- **Dashboard** — Full profile view (Knowledge, Skills, Curiosity, Personality, Library, Disclosure). **Browser only.** Served on GitHub Pages.
- **Q&A Mini App** — Interactive Q&A with Grace-Mar. Runs as a **Telegram Mini App** and can also be opened in a browser.

## Architecture

| Surface | Host | URL | Purpose |
|---------|------|-----|---------|
| Dashboard | GitHub Pages | `https://<org>.github.io/grace-mar/dashboard/` | Read-only fork view, browser-only |
| Q&A Mini App | Railway / Render / etc. | `https://grace-mar-qa.railway.app` | Ask Grace-Mar questions, see her knowledge and voice |

Set `DASHBOARD_MINIAPP_URL` in `bot/.env` to the **Q&A Mini App** URL (not the dashboard). The menu button and `/dashboard` open the Q&A app inside Telegram.

## 1. Dashboard (browser-only)

Generate and deploy the static dashboard:

```bash
python3 scripts/generate_dashboard.py
```

Deploy `dashboard/` to GitHub Pages via `.github/workflows/pages.yml`. The dashboard lives at `https://<org>.github.io/grace-mar/dashboard/`. Users open it directly in a browser.

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

Open http://localhost:5000. For Telegram testing, expose with ngrok:

```bash
ngrok http 5000
```

### Deploy (Railway / Render)

**Railway**

1. Connect the repo.
2. Root directory = repo root. Railway uses `Procfile` and `requirements.txt`.
3. Set env: `OPENAI_API_KEY`, `PORT` (optional, Railway sets it).
4. Deploy. Use the generated URL (e.g. `https://grace-mar-qa.railway.app`).

**Render**

- **Option A — Blueprint:** Add `render.yaml` to your repo. In Render Dashboard → New → Blueprint, connect the repo. Both the Mini App (web) and the bot (worker) will be created. Set env vars in each service’s Environment tab.
- **Option B — Manual:** New Web Service, connect repo. Build: `pip install -r requirements.txt`. Start: `python miniapp_server.py`. Set `OPENAI_API_KEY`, and optionally `GITHUB_TOKEN`, `GRACE_MAR_REPO`.

### Archive (optional)

Mini App exchanges are archived to `users/pilot-001/ARCHIVE.md`, the same file as Telegram and WeChat (one mind, multiple channels). Render’s filesystem is ephemeral, so the server uses the GitHub API to append to the repo.

Set these env vars on Render (or in `.env` locally):

- `GITHUB_TOKEN` — A fine-grained or classic PAT with `contents: write` on the repo
- `GRACE_MAR_REPO` — Repo in `owner/repo` form (default: `rbtkhn/grace-mar`)

Without them, local dev writes to `users/pilot-001/ARCHIVE.md` on disk; on Render, exchanges are not archived.

## 3. Bot (Webhook Mode)

The `render.yaml` blueprint runs the Telegram bot via **webhook** on the miniapp service (no separate worker). Set these env vars on the **miniapp** service:

- `TELEGRAM_BOT_TOKEN` — from @BotFather (when set, webhook is enabled)
- `OPENAI_API_KEY`
- `DASHBOARD_MINIAPP_URL` — your Mini App URL (e.g. `https://grace-mar-miniapp.onrender.com`)
- `GITHUB_TOKEN` — PAT with `contents: write` (for archiving to ARCHIVE.md)

See [TELEGRAM-WEBHOOK-SETUP](TELEGRAM-WEBHOOK-SETUP.md) for details and migration from polling.

## 4. Bot env (local)

When running the bot locally, set in `bot/.env`:

```env
DASHBOARD_MINIAPP_URL=https://grace-mar-miniapp.onrender.com
```

This URL must serve the Q&A Mini App. When set, the bot exposes `/dashboard` and the menu button. On Render, set the same var in the bot service’s Environment tab.

## 5. @BotFather (optional)

In @BotFather → Bot Settings → Menu Button:

- Set URL to your Q&A Mini App URL (same as `DASHBOARD_MINIAPP_URL`).

## 6. Deep linking

Use `startapp` to open the Q&A app:

- `t.me/your_bot?startapp=` — opens the Q&A Mini App.

## Security

- The Q&A API is stateless and uses the same `SYSTEM_PROMPT` as the bot. No profile writes from the Mini App.
- For production, consider rate limiting and `initData` validation (HMAC-SHA-256 with bot token) if you need user verification.

# Telegram Mini App Setup

**Channel roles:**
- **HTML profile** — Read-only. View identity, pipeline, SKILLS, benchmarks. No input, no chat.
- **Telegram** — Bidirectional. User and Grace-Mar exchange messages; "we did X" invokes the pipeline. The primary conversation channel.

Grace-Mar has two web surfaces:

- **Dashboard** — Full profile view (Knowledge, Skills, Curiosity, Personality, Library, Disclosure). **Browser only, read-only.** Available at **https://grace-mar.com**.
- **Q&A Mini App** — Interactive Q&A with Grace-Mar. Runs as a **Telegram Mini App** and can also be opened in a browser. Bidirectional (ask questions, get answers).

## Architecture

| Surface | Host | URL | Purpose |
|---------|------|-----|---------|
| Dashboard (HTML) | grace-mar.com | **https://grace-mar.com** | Read-only — view profile, pipeline, SKILLS, disclosure |
| Q&A Mini App | Render / Railway / your host | e.g. `https://grace-mar.onrender.com/` | Bidirectional — ask Grace-Mar questions, see her voice |

The **profile** is at **https://grace-mar.com**. Set `PROFILE_MINIAPP_URL` (or `DASHBOARD_MINIAPP_URL`) to **https://grace-mar.com** so the Telegram menu button opens the profile. (If you prefer the menu button to open the Q&A Mini App instead, set it to that URL.)

## 1. Dashboard (browser-only, read-only)

The profile is available at **https://grace-mar.com**. Generate the static HTML with `scripts/generate_profile.py`; deploy via GitHub Pages (point grace-mar.com at the Pages site) or serve from your own host. **Full steps:** [PROFILE-DEPLOY.md](PROFILE-DEPLOY.md).

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

### Archive (session transcript)

Mini App exchanges are appended to `users/<user>/SESSION-TRANSCRIPT.md` (real-time log, same policy as Telegram). SELF-ARCHIVE is updated only when candidates are merged via `process_approved_candidates` (gated). No GitHub token is required for archiving.

On Render, the filesystem is ephemeral, so SESSION-TRANSCRIPT written by the Mini App is lost between deploys unless you add a separate step to persist it (e.g. push to repo). Local dev writes to disk as usual.

## 3. Bot (Webhook Mode)

The `render.yaml` blueprint runs the Telegram bot via **webhook** on the miniapp service (no separate worker). Set these env vars on the **miniapp** service:

- `TELEGRAM_BOT_TOKEN` — from @BotFather (when set, webhook is enabled)
- `OPENAI_API_KEY`
- `PROFILE_MINIAPP_URL` — URL opened by the Telegram menu button (e.g. **https://grace-mar.com** for the profile); `DASHBOARD_MINIAPP_URL` still supported
- Session transcript is written locally; SELF-ARCHIVE is updated only on merge (no GITHUB_TOKEN needed for archiving).

See [TELEGRAM-WEBHOOK-SETUP](TELEGRAM-WEBHOOK-SETUP.md) for details and migration from polling.

## 4. Bot env (local)

When running the bot locally, set in `bot/.env`:

```env
PROFILE_MINIAPP_URL=https://grace-mar.com
# or DASHBOARD_MINIAPP_URL=https://grace-mar.com
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

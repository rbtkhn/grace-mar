# Telegram Webhook Setup

The Grace-Mar Telegram bot can run in two modes:

| Mode | When to use | Conflict risk |
|------|-------------|---------------|
| **Polling** | Local development | Only one instance; stops when you run on Render |
| **Webhook** | Production (Render, Railway) | None — Telegram pushes to your URL |

Webhook mode is recommended for production. It eliminates the "Conflict: terminated by other getUpdates request" error.

---

## How It Works

1. **Miniapp server** receives Telegram updates at `POST /telegram/webhook`
2. **Render** sets `RENDER_EXTERNAL_URL` automatically (e.g. `https://grace-mar-miniapp.onrender.com`)
3. **On startup**, the server registers the webhook with Telegram: `setWebhook(RENDER_EXTERNAL_URL/telegram/webhook)`
4. **Telegram** pushes updates to that URL instead of you polling

No separate bot worker. One web service handles both the Mini App and Telegram.

---

## Render Setup

The `render.yaml` blueprint configures the miniapp with optional Telegram webhook. Set these env vars on the **grace-mar-miniapp** service:

| Env var | Required | Description |
|---------|----------|-------------|
| `TELEGRAM_BOT_TOKEN` | Yes (for bot) | From @BotFather |
| `OPENAI_API_KEY` | Yes | For LLM responses |
| `DASHBOARD_MINIAPP_URL` | No | Q&A Mini App URL for bot menu button (e.g. `https://grace-mar.onrender.com`) |
| `GITHUB_TOKEN` | No | For archiving to VOICE-ARCHIVE.md |
| `GRACE_MAR_REPO` | No | Repo for archive (default: rbtkhn/grace-mar) |

**Do not** create a separate Background Worker for the bot. The miniapp handles it.

`RENDER_EXTERNAL_URL` is set automatically by Render — no need to add it.

---

## Migrating from Polling (Worker) to Webhook

If you previously had a **grace-mar-bot** worker:

1. **Remove** the worker service (or stop it) in the Render dashboard
2. **Add** `TELEGRAM_BOT_TOKEN` to the miniapp service
3. **Add** `DASHBOARD_MINIAPP_URL` to the miniapp (same as the miniapp URL)
4. **Redeploy** the miniapp

The miniapp will register the webhook on startup. The bot will work immediately.

---

## Local Development

- **With webhook locally:** Use ngrok to expose your machine, set `WEBHOOK_BASE_URL=https://your-ngrok-url.ngrok.io`, run `python miniapp_server.py`
- **With polling:** Run `python -m bot.bot` (or `python bot/bot.py`) — but **do not** run the bot on Render at the same time, or you'll get a conflict

---

## Clearing the Webhook (Troubleshooting)

If something goes wrong, clear the webhook and restart:

```bash
curl "https://api.telegram.org/bot<YOUR_BOT_TOKEN>/deleteWebhook"
```

Then redeploy the miniapp. It will re-register the webhook on startup.

---

*Last updated: February 2026*

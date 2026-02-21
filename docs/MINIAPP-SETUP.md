# Telegram Mini App Setup

The Grace-Mar dashboard can run as a **Telegram Mini App**, embedded inside Telegram so you can view the fork (profile, pipeline, benchmarks, disclosure) without leaving the chat.

## Prerequisites

- The dashboard must be served over **HTTPS**. Telegram only loads Mini Apps from secure origins.
- You need a hosted URL (e.g. GitHub Pages, Netlify, Vercel) pointing to the `dashboard/` directory.

## 1. Generate the dashboard

```bash
python3 scripts/generate_dashboard.py
```

This writes `dashboard/index.html`. The same file works both as a standalone page and as a Mini App.

## 2. Host the dashboard

Deploy `dashboard/` to a static host. Examples:

### GitHub Pages

A workflow (`.github/workflows/pages.yml`) builds and deploys the dashboard automatically:

1. Go to repo **Settings → Pages**.
2. Under "Build and deployment", set **Source** to **GitHub Actions** (not "Deploy from a branch").
3. Push to `main` or run the workflow manually (Actions → Deploy dashboard to Pages → Run workflow).
4. When deployment finishes, the site URL is `https://<org-or-username>.github.io/grace-mar/` (the dashboard is served at the root).
5. Set `DASHBOARD_MINIAPP_URL=https://<org-or-username>.github.io/grace-mar/` in `bot/.env`.

### Netlify / Vercel

1. Connect the repo.
2. Set the publish directory to `dashboard` (or the repo root and ensure `/dashboard/` is served).
3. Use the deployed URL, e.g. `https://grace-mar-dashboard.netlify.app/`.

## 3. Configure @BotFather (optional)

In @BotFather, you can set the Mini App URL as the **Menu Button**:

1. Open @BotFather and select your bot.
2. Bot Settings → Menu Button → Configure menu button.
3. Set the URL to your hosted dashboard, e.g. `https://username.github.io/grace-mar/dashboard/`.

This makes the menu button (next to the chat input) open the dashboard directly.

## 4. Configure the bot (.env)

Add the Mini App URL to `bot/.env`:

```
DASHBOARD_MINIAPP_URL=https://yourdomain.com/grace-mar/dashboard/
```

When set, the bot will:

- Expose `/dashboard` — sends an "Open Dashboard" button that launches the Mini App.
- Set the chat menu button to "Dashboard" so users can open it from the menu.

If `DASHBOARD_MINIAPP_URL` is not set, `/dashboard` will explain that setup is required.

## 5. Deep linking

You can open specific tabs via the `startapp` parameter:

- `t.me/your_bot?startapp=disclosure` — opens the Disclosure tab.
- `t.me/your_bot?startapp=knowledge` — opens the Knowledge tab.
- Valid tab IDs: `knowledge`, `skills`, `curiosity`, `personality`, `library`, `disclosure`.

Configure these links in @BotFather (Menu Button → URL) or in buttons/messages.

## Security

- The dashboard is read-only. No sensitive data is submitted from the Mini App.
- If you add forms or actions later, validate `initData` server-side with HMAC-SHA-256 using your bot token (see [Telegram Mini Apps docs](https://core.telegram.org/bots/webapps#validating-data-received-via-the-mini-app)).

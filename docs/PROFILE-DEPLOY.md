# Deploy the profile to grace-mar.com

The profile is static HTML generated from the pilot profile. To serve it at **https://grace-mar.com**, use GitHub Pages with a custom domain. **Domains (grace-mar.com, companion-self.com) are registered with Namecheap** — DNS steps below use Namecheap’s Advanced DNS.

---

## 1. One-time: Enable GitHub Pages and custom domain

### 1.1 Turn on Pages

1. In your repo: **Settings** → **Pages** (under “Code and automation”).
2. Under **Build and deployment**:
   - **Source:** Deploy from a branch.
   - **Branch:** `gh-pages` / `/(root)`.
3. Save. The site will be available at `https://<org>.github.io/grace-mar/` (or your user/org URL) once the workflow has run.

### 1.2 Add grace-mar.com as custom domain

1. Still in **Settings** → **Pages**.
2. Under **Custom domain**, enter: `grace-mar.com`.
3. Click **Save**. GitHub will show the DNS records you need.

### 1.3 Configure DNS at your registrar

Where you manage grace-mar.com (e.g. **Namecheap**, Cloudflare, Google Domains):

#### Namecheap (grace-mar.com, companion-self.com)

1. Log in at [namecheap.com](https://www.namecheap.com) → **Domain List** → click **Manage** next to the domain.
2. Open the **Advanced DNS** tab.
3. **For apex (grace-mar.com)** — Add four **A Record** entries:
   - Host: `@` | Type: `A Record` | Value: `185.199.108.153`  | TTL: Automatic
   - Host: `@` | Type: `A Record` | Value: `185.199.109.153`  | TTL: Automatic
   - Host: `@` | Type: `A Record` | Value: `185.199.110.153`  | TTL: Automatic
   - Host: `@` | Type: `A Record` | Value: `185.199.111.153`  | TTL: Automatic  
   Remove any existing **URL Redirect** or **A Record** for `@` if they conflict.
4. **Optional — www redirect:** If you want `www.grace-mar.com` to work, add a **CNAME Record**: Host `www` → Value `rbtkhn.github.io` (or `<your-org>.github.io`). Then in GitHub Pages you can add `www.grace-mar.com` as well, or use Namecheap’s “URL Redirect” to send www to grace-mar.com.
5. Save. DNS can take 5–30 minutes to propagate.

Repeat the same A records for **companion-self.com** (or another host) if you point that domain at a different service later.

#### Other registrars

**Option A — Apex domain (grace-mar.com):**

- Add **A** records pointing to GitHub’s IPs. GitHub shows these in the Pages custom-domain section; as of 2024 they are:
  - `185.199.108.153`
  - `185.199.109.153`
  - `185.199.110.153`
  - `185.199.111.153`

**Option B — Subdomain (e.g. www.grace-mar.com):**

- Add a **CNAME** record: `www` → `<org>.github.io` (or `rbtkhn.github.io` if it’s a user repo). Then in GitHub Pages custom domain, use `www.grace-mar.com` instead of `grace-mar.com`.

**If you use Cloudflare:** Turn **Proxy** (orange cloud) off for the A or CNAME record so GitHub can validate and serve the site, or use “DNS only”.

Wait for DNS to propagate (minutes to a few hours). Back in **Settings** → **Pages**, GitHub will show “DNS check successful” and will issue an HTTPS certificate for grace-mar.com.

---

## 2. Deploy the profile (every time you want to update)

The workflow `.github/workflows/pages.yml` builds and deploys the profile on every push to `main` **when profile-relevant files change** (e.g. `users/grace-mar/`, `scripts/generate_profile.py`). Pushes that only touch docs or other paths skip the deploy. You can also run the workflow manually.

### Fast loop — Local preview (seconds, no push)

See profile changes immediately without pushing:

```bash
python3 scripts/generate_profile.py
open profile/index.html   # macOS; on Linux: xdg-open profile/index.html
```

Or use the preview script (generates + opens):

```bash
./scripts/preview_profile.sh
```

When you’re happy, push to `main`; the workflow will run and update grace-mar.com in about a minute.

### Option A — Push to main

```bash
git add -A
git commit -m "Update profile"
git push origin main
```

The **Deploy profile to Pages** workflow runs, runs `python3 scripts/generate_profile.py`, and publishes the `profile/` folder to the `gh-pages` branch. In a minute or two, https://grace-mar.com will show the new content.

### Option B — Run the workflow manually

1. **Actions** → **Deploy profile to Pages** → **Run workflow** → **Run workflow**.
2. The workflow uses the current `main`; it will generate the profile and update `gh-pages`.

### Option C — Build and push gh-pages yourself

If you don’t want to use the workflow:

```bash
python3 scripts/generate_profile.py
git checkout gh-pages   # or create branch: git checkout -b gh-pages
git add profile/
git commit -m "Profile update"
git push origin gh-pages
git checkout main
```

---

## 3. Verify

- **https://grace-mar.com** — Landing page with buttons: Profile, Telegram, WeChat, LLM.
- **https://grace-mar.com/profile** — Full profile view (identity, pipeline, SKILLS, benchmarks).
- **https://grace-mar.com/telegram** — If configured, opens the Telegram chat with your Grace-Mar bot (instant redirect to `t.me/YourBotUsername`). To enable: create `users/grace-mar/TELEGRAM_BOT_USERNAME.txt` with one line, your bot’s username from @BotFather (e.g. `MyGraceMarBot`, no `@`). Regenerate the profile and redeploy.
- **https://grace-mar.com/llm** — Full PRP prompt text only, one-tap copy. Paste into any LLM (ChatGPT, Claude, etc.). Content is from `grace-mar-llm.txt`; regenerate with `export_prp.py` and redeploy to refresh.
- **https://grace-mar.com/wechat** — If configured, redirects to your WeChat Official Account URL (e.g. mp.weixin.qq.com link). Add the URL in one line to `users/grace-mar/WECHAT_ACCOUNT_URL.txt`, regenerate the profile, and redeploy. See `bot/WECHAT-SETUP.md`.
- **https://grace-mar.com/playlist** — Placeholder; playlist feature coming later.
- In the Telegram bot, set `PROFILE_MINIAPP_URL=https://grace-mar.com` (or `DASHBOARD_MINIAPP_URL`) so the menu button opens this URL.

---

## 4. Troubleshooting

| Issue | What to do |
|-------|------------|
| “DNS check failed” | Wait longer for DNS; ensure A or CNAME matches what GitHub shows. **Namecheap:** Use Advanced DNS (not “Redirect Domain”); remove conflicting URL Redirect or A records for `@`. If using Cloudflare, try DNS only (grey cloud). |
| 404 after deploy | Confirm Pages source is branch `gh-pages`, folder `/ (root)`. Confirm the workflow ran and updated `gh-pages`. |
| Old content still showing | Hard refresh (Ctrl+Shift+R / Cmd+Shift+R) or wait for CDN; re-run the workflow if needed. |
| Certificate / “Not secure” | GitHub provisions HTTPS for the custom domain after DNS validates; can take up to an hour. |

---

**See also:** [NAMECHEAP-GUIDE.md](NAMECHEAP-GUIDE.md) (simple Namecheap steps), [MINIAPP-SETUP.md](MINIAPP-SETUP.md) (profile vs Q&A app), [TELEGRAM-WEBHOOK-SETUP.md](TELEGRAM-WEBHOOK-SETUP.md) (bot menu button).

---

## 5. Accelerating the loop (HTML ↔ Cursor ↔ Telegram)

| What you want | What to do |
|---------------|------------|
| **See profile changes in seconds** | Run `./scripts/preview_profile.sh` (or `python3 scripts/generate_profile.py` then `open profile/index.html`). No push required. |
| **Deploy only when profile changes** | The workflow runs only when `users/grace-mar/**`, `scripts/generate_profile.py`, or the workflow file change. Doc-only pushes skip the deploy. |
| **Re-run deploy without a new commit** | **Actions** → **Deploy profile to Pages** → **Run workflow**. Uses current `main`. |
| **Telegram → Cursor** | If the bot runs **locally** (e.g. `python -m bot.bot`), SESSION-TRANSCRIPT, PENDING-REVIEW, and archive updates land in your repo immediately. If it runs on a server (e.g. Render), you need a sync step (e.g. pull from server or run the bot locally for development) so Cursor and the profile see the latest. |

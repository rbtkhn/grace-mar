# Deploy the dashboard to grace-mar.com

The dashboard is static HTML generated from the pilot profile. To serve it at **https://grace-mar.com**, use GitHub Pages with a custom domain.

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

Where you manage grace-mar.com (e.g. Cloudflare, Namecheap, Google Domains):

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

## 2. Deploy the dashboard (every time you want to update)

The workflow `.github/workflows/pages.yml` builds and deploys the dashboard on every push to `main`.

### Option A — Push to main

```bash
git add -A
git commit -m "Update profile / dashboard"
git push origin main
```

The **Deploy dashboard to Pages** workflow runs, runs `python3 scripts/generate_dashboard.py`, and publishes the `dashboard/` folder to the `gh-pages` branch. In a minute or two, https://grace-mar.com will show the new content.

### Option B — Run the workflow manually

1. **Actions** → **Deploy dashboard to Pages** → **Run workflow** → **Run workflow**.
2. The workflow uses the current `main`; it will generate the dashboard and update `gh-pages`.

### Option C — Build and push gh-pages yourself

If you don’t want to use the workflow:

```bash
python3 scripts/generate_dashboard.py
git checkout gh-pages   # or create branch: git checkout -b gh-pages
git add dashboard/
git commit -m "Dashboard update"
git push origin gh-pages
git checkout main
```

---

## 3. Verify

- Open **https://grace-mar.com**. You should see the Grace-Mar dashboard (profile, pipeline, SKILLS, benchmarks).
- In the Telegram bot, set `DASHBOARD_MINIAPP_URL=https://grace-mar.com` so the menu button opens this URL.

---

## 4. Troubleshooting

| Issue | What to do |
|-------|------------|
| “DNS check failed” | Wait longer for DNS; ensure A or CNAME matches what GitHub shows; if using Cloudflare, try DNS only (grey cloud). |
| 404 after deploy | Confirm Pages source is branch `gh-pages`, folder `/ (root)`. Confirm the workflow ran and updated `gh-pages`. |
| Old content still showing | Hard refresh (Ctrl+Shift+R / Cmd+Shift+R) or wait for CDN; re-run the workflow if needed. |
| Certificate / “Not secure” | GitHub provisions HTTPS for the custom domain after DNS validates; can take up to an hour. |

---

**See also:** [MINIAPP-SETUP.md](MINIAPP-SETUP.md) (dashboard vs Q&A app), [TELEGRAM-WEBHOOK-SETUP.md](TELEGRAM-WEBHOOK-SETUP.md) (bot menu button).

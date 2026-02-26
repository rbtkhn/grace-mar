# Namecheap — What to do

**Domains:** grace-mar.com, companion-self.com (registered with Namecheap)

Use this when you need to point a domain at a host (e.g. GitHub Pages for the profile).

---

## Point grace-mar.com at GitHub Pages (profile)

1. Log in at **namecheap.com** → **Domain List** → click **Manage** next to **grace-mar.com**.

2. Open the **Advanced DNS** tab.

3. Remove any **URL Redirect** or **A Record** that uses Host `@` (so GitHub can control the apex).

4. Add **4 A records** (click **Add New Record** for each):

   | Type   | Host | Value            | TTL        |
   |--------|------|------------------|------------|
   | A Record | @  | 185.199.108.153  | Automatic  |
   | A Record | @  | 185.199.109.153  | Automatic  |
   | A Record | @  | 185.199.110.153  | Automatic  |
   | A Record | @  | 185.199.111.153  | Automatic  |

   **What this means:**
   - **A record** — Tells the internet: “When someone visits this domain, send them to this server.” You’re giving the numeric address (IP) of GitHub’s servers.
   - **Host `@`** — Means “the main domain with no prefix.” So this applies to **grace-mar.com** (not www.grace-mar.com or something else). In Namecheap you literally choose or type `@` in the Host field.
   - **The four IPs** — Those numbers are GitHub’s servers. **Source:** [GitHub Docs — Managing a custom domain for your GitHub Pages site](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-a-custom-domain-for-your-github-pages-site). GitHub publishes these IPs for apex domains; if they ever change, that page has the current ones. You add one A record per IP (four rows total).
   - **TTL Automatic** — How long other servers can cache this answer. “Automatic” is fine; Namecheap will pick a reasonable value.

5. Click **Save**. Wait 5–30 minutes for DNS to update.

6. In GitHub: repo → **Settings** → **Pages** → **Custom domain** → type `grace-mar.com` → **Save**. GitHub will check DNS and enable HTTPS.

Done. The profile at grace-mar.com will serve from GitHub Pages once the **Deploy profile to Pages** workflow has run (it runs on push to `main`).

---

## Optional: www.grace-mar.com

If you want `www.grace-mar.com` to work too:

- Add one **CNAME Record**: Host `www` → Value `rbtkhn.github.io` (or your GitHub username/organization).  
- In GitHub Pages custom domain you can add `www.grace-mar.com` as well, or use Namecheap’s **URL Redirect** to send www → grace-mar.com.

---

## companion-self.com

Use the same idea when you’re ready to use companion-self.com:

- **GitHub Pages:** Same 4 A records for `@`, Value = the four IPs above; then set custom domain in the repo that will serve it.
- **Another host (e.g. Render, Netlify):** Follow that host’s “custom domain” instructions; they’ll tell you whether to use A records or a CNAME and what to put in Namecheap.

---

**See also:** [profile-deploy.md](profile-deploy.md) for the full deploy steps (GitHub Pages, workflow, troubleshooting).

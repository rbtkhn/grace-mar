# Predictive History — reader site (static)

**Purpose:** A **Jiang-first** landing page for students, YouTube viewers, and Substack readers. It elevates **Professor Jiang Xueqin’s** public teaching and writing; the copy states clearly that **authorship of the ideas is Jiang’s**, and that this repo’s book layers are **curated presentation** alongside the channel and newsletter.

## Files

| File | Role |
|------|------|
| `index.html` | Single-page site: hero, attribution strip, audience paths, volume grid, book pointers |
| `assets/styles.css` | Typography and layout (serif + sans; light/dark via `prefers-color-scheme`) |

## View locally

Relative links to `../lectures/`, `../book/`, etc. resolve when the **parent** directory is the HTTP root.

From `research/external/work-jiang/`:

```bash
python3 -m http.server 8765
```

Then open: `http://127.0.0.1:8765/site/`

Opening `index.html` directly (`file://`) may break relative links to parent folders; use a local server.

## Deploy

Any static host (GitHub Pages, Netlify, Cloudflare Pages) works. If the site is deployed at a **subpath**, set a `<base href="...">` or adjust relative links in `index.html`.

## Relation to the repo

- Documented from [work-jiang README](../README.md) and [PUBLISHING.md](../book/PUBLISHING.md).
- Does **not** merge into the companion Record; operator / WORK lane only.

# Applied Theology — website

Static single-page site that presents the full text of *Applied Theology* with a clear table of contents and readable typography.

## Build

From this directory:

```bash
pip install markdown   # if not already installed
python3 build.py
```

This reads `../APPLIED-THEOLOGY.md` and writes `index.html`. Re-run after editing the book source.

## View

- **Local:** Open `index.html` in a browser, or run a static server, e.g. `python3 -m http.server 8000` then visit `http://localhost:8000`.
- **Deploy:** Upload the contents of this folder (index.html, styles.css, script.js) to any static host (GitHub Pages, Netlify, etc.).

## Files

| File        | Purpose |
|------------|---------|
| `build.py` | Converts APPLIED-THEOLOGY.md to HTML, wraps parts in sections, outputs index.html |
| `index.html` | Generated; do not edit by hand |
| `styles.css` | Typography, layout, sidebar nav, responsive rules |
| `script.js` | Nav toggle (mobile), active section highlight on scroll |

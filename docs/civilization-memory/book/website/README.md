# Beauty and the Blade — website

Static single-page site that presents the full text of *Beauty and the Blade* (*A Symphony of Civilizations*) from `APPLIED-THEOLOGY.md`, with a chapter-aligned table of contents, reading progress, and readable typography.

## Build

From this directory:

```bash
pip install markdown   # if not already installed
python3 build.py --force   # always rebuild
# or: python3 build.py     # skip if index.html is newer than APPLIED-THEOLOGY.md
```

`build.py` splits the manuscript on anchors (`# Prelude`, `# Chapter N`, `## Ten Axioms of Divinity`, etc.). If those headings change in `APPLIED-THEOLOGY.md`, update `SECTION_BOUNDARIES` in `build.py`.

## View

- **Local:** Open `index.html` in a browser, or run a static server, e.g. `python3 -m http.server 8000` then visit `http://localhost:8000`.
- **Deploy:** Upload the contents of this folder (index.html, styles.css, script.js) to any static host (GitHub Pages, Netlify, etc.).

## Files

| File        | Purpose |
|------------|---------|
| `build.py` | Splits APPLIED-THEOLOGY.md by chapter, converts to HTML, writes index.html |
| `index.html` | Generated; do not edit by hand |
| `styles.css` | Typography, layout, sidebar nav, reading progress bar, back-to-top |
| `script.js` | Nav toggle (mobile), active section on scroll, progress bar, back-to-top |

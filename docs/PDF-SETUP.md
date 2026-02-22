# PDF Setup — White Paper & Business Prospectus

Render the Grace-Mar White Paper and Business Prospectus to visually compelling PDFs using Pandoc and the Eisvogel LaTeX template.

---

## Option A: Bundled Tools (No Homebrew)

If you don't have Homebrew, use the bundled Pandoc and Tectonic:

```bash
./scripts/setup_pdf_tools.sh         # One-time: downloads Pandoc + Tectonic to tools/
./scripts/render_pdf.sh --install-eisvogel   # One-time: install Eisvogel template
./scripts/render_pdf.sh              # Render PDFs
```

---

## Option B: Homebrew

1. **Pandoc** — `brew install pandoc`
2. **LaTeX** — `brew install --cask mactex-no-gui` (~4 GB) or `basictex` (~100 MB)
3. **Eisvogel** — `./scripts/render_pdf.sh --install-eisvogel`

---

## Usage

```bash
./scripts/render_pdf.sh
```

Outputs:
- `docs/WHITE-PAPER.pdf`
- `docs/BUSINESS-PROSPECTUS.pdf`

To write PDFs elsewhere:
```bash
OUTPUT_DIR=./dist ./scripts/render_pdf.sh
```

---

## What You Get

- **Typography** — Eisvogel provides clean, professional layout
- **Table of contents** — Auto-generated from headings
- **Numbered sections** — Easy navigation
- **Hyperlinks** — Clickable cross-references
- **Metadata** — Title, subtitle, author, date on cover

---

## Without Eisvogel

The script falls back to Pandoc's default template if Eisvogel is not installed. Output is still readable but less polished. Run `--install-eisvogel` for best results.

## Bundled vs System

The script prefers system-installed `pandoc` and `xelatex` when available. If not found, it uses `tools/pandoc-*/bin/pandoc` and `tools/tectonic` (installed by `setup_pdf_tools.sh`). Tectonic is a self-contained LaTeX engine that fetches packages on demand — no MacTeX/BasicTeX required.

---

## Troubleshooting

| Issue | Fix |
|-------|-----|
| `xelatex not found` | Add LaTeX to PATH: `eval "$(/usr/libexec/path_helper -s)"` or restart terminal after installing MacTeX |
| `! LaTeX Error: File '...' not found` | Install missing LaTeX packages: `sudo tlmgr install <package>` |
| Eisvogel download fails | Download [Eisvogel release](https://github.com/Wandmalfarbe/pandoc-latex-template/releases) manually, extract `eisvogel.tex` to `~/.local/share/pandoc/templates/eisvogel.latex` |

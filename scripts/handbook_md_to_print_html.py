#!/usr/bin/env python3
"""Convert a work-politics handbook .md to print-friendly HTML (tables + links)."""

from __future__ import annotations

import argparse
import re
from pathlib import Path

import markdown

REPO = Path(__file__).resolve().parent.parent

PRINT_CSS = """
@page { margin: 1.2cm; }
body {
  font-family: system-ui, -apple-system, "Segoe UI", Roboto, sans-serif;
  font-size: 11pt;
  line-height: 1.45;
  color: #111;
  max-width: 48rem;
  margin: 0 auto;
  padding: 1rem;
}
h1 { font-size: 1.35rem; margin-top: 0; }
h2 { font-size: 1.1rem; margin-top: 1.25rem; border-bottom: 1px solid #ddd; padding-bottom: 0.2rem; }
table { border-collapse: collapse; width: 100%; margin: 0.75rem 0; font-size: 10pt; }
th, td { border: 1px solid #ccc; padding: 0.35rem 0.5rem; text-align: left; vertical-align: top; }
th { background: #f5f5f5; }
a { color: #0b57d0; word-break: break-all; }
hr { border: none; border-top: 1px solid #ddd; margin: 1rem 0; }
@media print {
  a { color: #000; text-decoration: none; }
  a[href^="http"]::after { content: " (" attr(href) ")"; font-size: 8pt; color: #444; }
}
"""


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("input_md", type=Path, help="Path to .md file")
    p.add_argument("-o", "--output", type=Path, help="Output .html (default: same stem .html)")
    args = p.parse_args()
    md_path = args.input_md.resolve()
    if not md_path.exists():
        print(f"Not found: {md_path}", flush=True)
        return 1
    out = args.output or md_path.with_suffix(".html")
    text = md_path.read_text(encoding="utf-8")
    # Resolve relative links in handbook to repo-relative paths for file:// viewing
    body = markdown.markdown(
        text,
        extensions=["tables", "fenced_code", "nl2br"],
    )
    title_match = re.search(r"<h1>([^<]+)</h1>", body)
    title = title_match.group(1).strip() if title_match else md_path.stem
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <style>{PRINT_CSS}</style>
</head>
<body>
{body}
<p style="margin-top:2rem;font-size:9pt;color:#666;">Generated from <code>{md_path.relative_to(REPO)}</code> — open this file in a browser and use Print → Save as PDF.</p>
</body>
</html>
"""
    out.write_text(html, encoding="utf-8")
    print(f"Wrote {out}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

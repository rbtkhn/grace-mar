#!/usr/bin/env python3
"""
Build the Beauty and the Blade website from APPLIED-THEOLOGY.md.
Splits on chapter anchors (# Prelude, # Chapter N, ## Ten Axioms, etc.).
Requires: pip install markdown
"""
import re
import sys
from pathlib import Path

try:
    import markdown
except ImportError:
    print("Run: pip install markdown", file=sys.stderr)
    sys.exit(1)

BOOK_DIR = Path(__file__).resolve().parent.parent
MD_PATH = BOOK_DIR / "APPLIED-THEOLOGY.md"
OUT_PATH = Path(__file__).resolve().parent / "index.html"

# (section_id, nav_label, start_marker, end_marker or None for EOF)
SECTION_BOUNDARIES = [
    ("intro", "Front matter", None, "# Prelude — Beauty and the Blade"),
    (
        "promise",
        "Prelude & Ch. 1 — The Simple Condition",
        "# Prelude — Beauty and the Blade",
        "# Chapter 2 — One Subject, Many Tongues",
    ),
    (
        "chapter-2",
        "Ch. 2 — One Subject, Many Tongues",
        "# Chapter 2 — One Subject, Many Tongues",
        "# Chapter 3 — Only Through Love",
    ),
    (
        "chapter-3",
        "Ch. 3 — Only Through Love",
        "# Chapter 3 — Only Through Love",
        "# Chapter 4 — The Focal Point",
    ),
    (
        "chapter-4",
        "Ch. 4 — The Focal Point",
        "# Chapter 4 — The Focal Point",
        "# Chapter 5 — The Delusion of Separation",
    ),
    (
        "chapter-5",
        "Ch. 5 — The Delusion of Separation",
        "# Chapter 5 — The Delusion of Separation",
        "# Chapter 6 — The Gate",
    ),
    (
        "chapter-6",
        "Ch. 6 — The Gate (AI ethics)",
        "# Chapter 6 — The Gate",
        "# Chapter 7 — The Most Interesting Activity",
    ),
    (
        "chapter-7",
        "Ch. 7 — Writing the Book and Death",
        "# Chapter 7 — The Most Interesting Activity",
        "# Chapter 8 — Expand the Light",
    ),
    (
        "chapter-8",
        "Ch. 8 — Preserving Consciousness",
        "# Chapter 8 — Expand the Light",
        "# Chapter 9 — Heaven or Armageddon",
    ),
    (
        "chapter-9",
        "Ch. 9 — Scripture as Test",
        "# Chapter 9 — Heaven or Armageddon",
        "## Ten Axioms of Divinity",
    ),
    (
        "axioms",
        "Ten Axioms of Divinity",
        "## Ten Axioms of Divinity",
        "## Appendix — How to run a seam audit",
    ),
    (
        "appendix",
        "Appendix — Seam audit",
        "## Appendix — How to run a seam audit",
        "## Limits and acknowledgments",
    ),
    ("limits", "Limits & acknowledgments", "## Limits and acknowledgments", None),
]

META_DESCRIPTION = (
    "Beauty and the Blade — peace as condition for what the world's traditions await; "
    "the seam between mercy and violence; one reference, many tongues; ten axioms of divinity "
    "major religions can test in their own language."
)


def split_sections(text):
    """Return [(section_id, markdown_block), ...]."""
    sections = []
    for sid, _label, start_m, end_m in SECTION_BOUNDARIES:
        if start_m is None:
            start = 0
        else:
            start = text.find(start_m)
            if start == -1:
                print(f"ERROR: start marker not found: {start_m!r}", file=sys.stderr)
                sys.exit(1)
        if end_m is None:
            end = len(text)
        else:
            end = text.find(end_m, start + len(start_m) if start_m else 1)
            if end == -1:
                print(f"ERROR: end marker not found after {sid}: {end_m!r}", file=sys.stderr)
                sys.exit(1)
        block = text[start:end].strip()
        if block:
            sections.append((sid, block))
    return sections


def md_to_html(md_text, section_id=""):
    """Convert markdown to HTML. Add ids to h2 and h3 for deep linking."""
    html = markdown.markdown(
        md_text,
        extensions=["extra"],
        extension_configs={"extra": {"enable_attributes": True}},
    )
    prefix = f"{section_id}-" if section_id else ""

    for level in ["h2", "h3"]:

        def repl(m, p=prefix):
            s = slug(m.group(2))
            return f'<{m.group(1)} id="{p}{s}">{m.group(2)}</{m.group(1)}>' if s else m.group(0)

        html = re.sub(rf"<({level})>([^<]+)</\1>", repl, html)
    return html


def slug(s):
    s = re.sub(r"[^\w\s-]", "", s)
    s = re.sub(r"[-\s]+", "-", s).strip("-").lower()
    return s[:80] if s else ""


def build_nav():
    return "\n".join(
        f'        <li><a href="#{sid}">{label}</a></li>'
        for sid, label, _, _ in SECTION_BOUNDARIES
    )


def main():
    force = "--force" in sys.argv
    if not MD_PATH.exists():
        print(f"Missing {MD_PATH}", file=sys.stderr)
        sys.exit(1)
    md_mtime = MD_PATH.stat().st_mtime
    if not force and OUT_PATH.exists() and OUT_PATH.stat().st_mtime >= md_mtime:
        print("Already up to date.")
        return
    md_content = MD_PATH.read_text(encoding="utf-8")
    sections = split_sections(md_content)

    body_sections = []
    for sid, block in sections:
        html_content = md_to_html(block, section_id=sid)
        body_sections.append(
            f'    <section id="{sid}" class="content-section">\n{html_content}\n    </section>'
        )

    nav_html = build_nav()
    sections_html = "\n\n".join(body_sections)
    esc_desc = (
        META_DESCRIPTION.replace("&", "&amp;")
        .replace('"', "&quot;")
        .replace("<", "&lt;")
    )

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Beauty and the Blade</title>
  <meta name="description" content="{esc_desc}">
  <meta property="og:title" content="Beauty and the Blade">
  <meta property="og:description" content="{esc_desc}">
  <meta property="og:type" content="book">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,600;1,400&family=Source+Sans+3:wght@400;600&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="styles.css">
</head>
<body>
  <div class="reading-progress" role="progressbar" aria-valuemin="0" aria-valuemax="100" aria-valuenow="0" aria-label="Reading progress"></div>
  <header class="site-header">
    <div class="header-inner">
      <h1 class="site-title">Beauty and the Blade</h1>
      <p class="site-subtitle">A Symphony of Civilizations</p>
      <p class="site-dek">Peace as the <strong>condition</strong> for what major traditions say they await — not the reward after. The <strong>seam</strong> between beauty and blade in every scripture; <strong>one reference, many tongues</strong>; and <strong>ten axioms of divinity</strong> you can test in your own language.</p>
      <p class="site-jump">
        <a href="#axioms">Jump to Ten Axioms</a>
        <span class="site-jump-sep">·</span>
        <a href="#promise">Start at Prelude &amp; letter</a>
      </p>
    </div>
  </header>

  <div class="layout">
    <nav class="sidebar" aria-label="Table of contents">
      <button type="button" class="nav-toggle" aria-expanded="false" aria-controls="nav-list">Contents</button>
      <ul id="nav-list" class="nav-list">
{nav_html}
      </ul>
    </nav>

    <main class="main-content" id="main-content">
{sections_html}
    </main>
  </div>

  <button type="button" class="back-to-top" aria-label="Back to top" hidden>↑</button>

  <footer class="site-footer">
    <p>No authority is claimed. Offered as a record of reflection and an invitation to test against your own tradition.</p>
  </footer>

  <script src="script.js"></script>
</body>
</html>
"""

    OUT_PATH.write_text(html, encoding="utf-8")
    print(f"Wrote {OUT_PATH}")


if __name__ == "__main__":
    main()

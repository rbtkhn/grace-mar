#!/usr/bin/env python3
"""
Build the Beauty and the Blade website from APPLIED-THEOLOGY.md.
Outputs index.html with nav and sectioned content.
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

NAV_ITEMS = [
    ("preface", "Preface"),
    ("part-1", "1. The Call"),
    ("part-2", "2. The Response"),
    ("part-3", "3. The Deepening"),
    ("part-4", "4. The Science"),
    ("part-5", "5. The Framework"),
    ("part-6", "6. The Use"),
    ("part-7", "7. The Coda"),
    ("part-8", "8. Preserving Consciousness"),
    ("part-9", "9. Scripture as Test"),
    ("appendix", "Appendix"),
]


def split_sections(text: str) -> list[tuple[str, str]]:
    """Split MD into (section_id, md_content) for preface, part-1..part-9, appendix."""
    sections = []
    # Match "# Part N" or "# Appendix"
    part_pattern = re.compile(r'^# (Part \d+|[Aa]ppendix)[^\n]*', re.MULTILINE)
    positions = [(m.start(), m.group(1)) for m in part_pattern.finditer(text)]

    def section_id(label: str) -> str:
        if label.lower().startswith("appendix"):
            return "appendix"
        n = re.search(r"\d+", label)
        return f"part-{n.group(0)}" if n else "preface"

    # Preface: everything before first "# Part 1"
    first_part_idx = next((i for i, (_, label) in enumerate(positions) if "Part 1" in label), None)
    if first_part_idx is not None:
        preface_end = positions[first_part_idx][0]
        preface_text = text[:preface_end].strip()
        if preface_text:
            sections.append(("preface", preface_text))

    # Parts and appendix: from each "# Part N" / "# Appendix" to the next
    for i, (start, label) in enumerate(positions):
        end = positions[i + 1][0] if i + 1 < len(positions) else len(text)
        block = text[start:end].strip()
        sid = section_id(label)
        sections.append((sid, block))

    return sections


def md_to_html(md_text: str, section_id: str = "") -> str:
    """Convert markdown to HTML. Add ids to h2, h3 for deep linking (prefixed by section_id)."""
    html = markdown.markdown(
        md_text,
        extensions=["extra"],
        extension_configs={"extra": {"enable_attributes": True}},
    )
    # Add slug ids to h2 and h3, prefixed by section to avoid duplicate ids
    prefix = f"{section_id}-" if section_id else ""
    for level in ["h2", "h3"]:
        def repl(m, p=prefix):
            s = slug(m.group(2))
            return f'<{m.group(1)} id="{p}{s}">{m.group(2)}</{m.group(1)}>' if s else m.group(0)
        html = re.sub(rf"<({level})>([^<]+)</\1>", repl, html)
    return html


def slug(s: str) -> str:
    """Simple slug from heading text."""
    s = re.sub(r"[^\w\s-]", "", s)
    s = re.sub(r"[-\s]+", "-", s).strip("-").lower()
    return s[:80] if s else ""  # allow longer for readability


def build_nav() -> str:
    return "\n".join(
        f'        <li><a href="#{sid}">{label}</a></li>' for sid, label in NAV_ITEMS
    )


def main() -> None:
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
        body_sections.append(f'    <section id="{sid}" class="content-section">\n{html_content}\n    </section>')

    nav_html = build_nav()
    sections_html = "\n\n".join(body_sections)

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Beauty and the Blade — A Symphony of Civilizations</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,600;1,400&family=Source+Sans+3:wght@400;600&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="styles.css">
</head>
<body>
  <header class="site-header">
    <div class="header-inner">
      <h1 class="site-title">Beauty and the Blade</h1>
      <p class="site-subtitle">A Symphony of Civilizations</p>
    </div>
  </header>

  <div class="layout">
    <nav class="sidebar" aria-label="Contents">
      <button type="button" class="nav-toggle" aria-expanded="false" aria-controls="nav-list">Contents</button>
      <ul id="nav-list" class="nav-list">
{nav_html}
      </ul>
    </nav>

    <main class="main-content">
{sections_html}
    </main>
  </div>

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

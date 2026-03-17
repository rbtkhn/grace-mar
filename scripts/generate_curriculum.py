#!/usr/bin/env python3
"""
Generate homeschool curriculum: HTML modules (with optional quiz links) + optional PDF.

Uses Record (IX-B curiosity, IX-A knowledge) and load_alpha_school_benchmarks for structure.
Output: curriculum/ directory with index.html and module-*.html; optional curriculum.pdf via Pandoc.

Usage:
    python scripts/generate_curriculum.py -u grace-mar
    python scripts/generate_curriculum.py -u grace-mar -o output/ --pdf
"""

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))
sys.path.insert(0, str(REPO_ROOT / "scripts"))


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def _ix_b_topics(self_content: str, limit: int = 10) -> list[str]:
    """Extract curiosity (IX-B) topic lines for curriculum themes."""
    topics = []
    in_ixb = False
    for line in self_content.splitlines():
        if "### IX-B" in line or "## IX-B" in line:
            in_ixb = True
            continue
        if in_ixb and "topic:" in line:
            m = re.search(r'topic:\s*["\']?([^"\'\n]+)', line)
            if m:
                topics.append(m.group(1).strip().strip('"')[:80])
            if len(topics) >= limit:
                break
        if in_ixb and (line.strip().startswith("##") or line.strip().startswith("###")) and "IX-C" in line:
            break
    return topics


def _ix_a_sample(self_content: str, limit: int = 15) -> list[str]:
    """Extract a few LEARN entry snippets for knowledge context."""
    samples = []
    for m in re.finditer(r"id:\s+LEARN-\d+\s*\n(.*?)(?=id:\s+LEARN-|\Z)", self_content, re.DOTALL):
        block = m.group(1).strip()[:200]
        if block:
            samples.append(block)
        if len(samples) >= limit:
            break
    return samples


def build_curriculum(user_id: str = "grace-mar", output_dir: Path | None = None) -> list[Path]:
    """Generate HTML modules and return list of written paths."""
    profile_dir = REPO_ROOT / "users" / user_id
    self_path = profile_dir / "self.md"
    self_content = _read(self_path)
    topics = _ix_b_topics(self_content)
    if not topics:
        topics = ["Reading", "Math", "Science", "Creative writing"]
    out = output_dir or REPO_ROOT / "curriculum"
    out.mkdir(parents=True, exist_ok=True)
    written = []
    index_lines = [
        "<!DOCTYPE html><html><head><meta charset='utf-8'><title>Curriculum</title></head><body>",
        "<h1>Curriculum modules</h1>",
        "<p>Generated from Record (IX-B curiosity, knowledge). Use with miniapp for Q&A.</p>",
        "<ul>",
    ]
    for i, topic in enumerate(topics[:10], 1):
        mod_path = out / f"module-{i}.html"
        mod_html = (
            f"<!DOCTYPE html><html><head><meta charset='utf-8'><title>Module {i}</title></head><body>"
            f"<h1>Module {i}: {topic}</h1>"
            f"<p>Theme: {topic}. Ask Grace-Mar about this in the Q&A miniapp.</p>"
            f"<p><a href='index.html'>Back to index</a></p></body></html>"
        )
        mod_path.write_text(mod_html, encoding="utf-8")
        written.append(mod_path)
        index_lines.append(f"<li><a href='module-{i}.html'>Module {i}: {topic}</a></li>")
    index_lines.append("</ul></body></html>")
    index_path = out / "index.html"
    index_path.write_text("\n".join(index_lines), encoding="utf-8")
    written.append(index_path)
    return written


def export_pdf(curriculum_dir: Path, output_pdf: Path) -> bool:
    """Export index.html to PDF via Pandoc if available."""
    import subprocess
    index_html = curriculum_dir / "index.html"
    if not index_html.exists():
        return False
    try:
        subprocess.run(
            ["pandoc", str(index_html), "-o", str(output_pdf)],
            cwd=str(curriculum_dir),
            check=True,
            capture_output=True,
        )
        return True
    except (FileNotFoundError, subprocess.CalledProcessError):
        return False


def main() -> int:
    import argparse
    ap = argparse.ArgumentParser(description="Generate curriculum HTML + optional PDF")
    ap.add_argument("-u", "--user", default="grace-mar")
    ap.add_argument("-o", "--output", default=None)
    ap.add_argument("--pdf", action="store_true", help="Export curriculum.pdf via Pandoc")
    args = ap.parse_args()
    out_dir = Path(args.output) if args.output else REPO_ROOT / "curriculum"
    paths = build_curriculum(user_id=args.user, output_dir=out_dir)
    print(f"Wrote {len(paths)} files to {out_dir}", file=sys.stderr)
    if args.pdf:
        pdf_path = out_dir / "curriculum.pdf"
        if export_pdf(out_dir, pdf_path):
            print(f"Wrote {pdf_path}", file=sys.stderr)
        else:
            print("Pandoc not found or PDF export failed; skip --pdf or install pandoc", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())

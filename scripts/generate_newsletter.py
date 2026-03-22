#!/usr/bin/env python3
"""
Generate a weekly digest (newsletter) from journal.md and optional curiosity (IX-B) snippets.

Pulls public-suitable journal entries and optionally curiosity dimension for a simple
markdown or HTML digest. Intended for cron (e.g. GitHub Actions weekly) that commits
to research/newsletter/ or sends via SendGrid/X.

Usage:
    python scripts/generate_newsletter.py
    python scripts/generate_newsletter.py --user grace-mar --output research/newsletter/digest-2026-03-16.md
    python scripts/generate_newsletter.py --format html --output research/newsletter/digest.html
"""

import argparse
import re
from datetime import datetime, timedelta
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def _parse_journal_entries(content: str) -> list[dict]:
    """Extract journal entries (date, entry, approved) from journal.md YAML."""
    entries = []
    in_entries = False
    for line in content.splitlines():
        if line.strip() == "entries:":
            in_entries = True
            continue
        if in_entries and line.strip().startswith("- date:"):
            m = re.search(r'date:\s*["\']?([^"\']+)["\']?', line)
            date_str = m.group(1).strip() if m else ""
            entries.append({"date": date_str, "entry": "", "approved": True})
            continue
        if in_entries and entries and line.strip().startswith("entry:"):
            m = re.search(r'entry:\s*["\'](.+)["\']', line)
            if m:
                entries[-1]["entry"] = m.group(1).strip()
        if in_entries and entries and "approved:" in line:
            entries[-1]["approved"] = "true" in line.lower()
    return [e for e in entries if e.get("approved") and e.get("entry")]


def _parse_curiosity_snippets(self_content: str, limit: int = 5) -> list[str]:
    """Extract recent curiosity (IX-B) topic lines for digest."""
    topics = []
    in_ixb = False
    for line in self_content.splitlines():
        if "### IX-B" in line or "## IX-B" in line:
            in_ixb = True
            continue
        if in_ixb and re.match(r"^\s*-\s+id:\s+CUR-", line):
            continue
        if in_ixb and "topic:" in line:
            m = re.search(r'topic:\s*["\']?([^"\'\n]+)', line)
            if m:
                topics.append(m.group(1).strip().strip('"'))
            if len(topics) >= limit:
                break
        if in_ixb and line.strip().startswith("##") or line.strip().startswith("###"):
            if "IX-C" in line or "IX-A" in line:
                break
    return topics


def build_digest(
    user_id: str = "grace-mar",
    days: int = 7,
    include_curiosity: bool = True,
) -> dict:
    """Build digest data from journal and optional self (IX-B)."""
    profile_dir = REPO_ROOT / "users" / user_id
    journal_path = profile_dir / "journal.md"
    self_path = profile_dir / "self.md"
    journal_raw = _read(journal_path)
    self_raw = _read(self_path) if include_curiosity else ""
    entries = _parse_journal_entries(journal_raw)
    cutoff = (datetime.now() - timedelta(days=days)).date().isoformat()
    recent = [e for e in entries if e.get("date", "") >= cutoff]
    curiosity = _parse_curiosity_snippets(self_raw) if include_curiosity else []
    return {
        "user_id": user_id,
        "generated_at": datetime.now().isoformat(),
        "days": days,
        "entries": recent,
        "curiosity": curiosity,
    }


def render_markdown(data: dict) -> str:
    """Render digest as Markdown."""
    lines = [
        f"# Grace-Mar digest — last {data['days']} days",
        "",
        f"*Generated {data['generated_at'][:10]}*",
        "",
    ]
    if data.get("entries"):
        lines.append("## Journal highlights")
        lines.append("")
        for e in data["entries"]:
            lines.append(f"**{e['date']}** — {e['entry']}")
            lines.append("")
    if data.get("curiosity"):
        lines.append("## Curiosity (IX-B)")
        lines.append("")
        for t in data["curiosity"]:
            lines.append(f"- {t}")
        lines.append("")
    if not data.get("entries") and not data.get("curiosity"):
        lines.append("No new entries in this period.")
    return "\n".join(lines)


def render_html(data: dict) -> str:
    """Render digest as minimal HTML."""
    body = "<h1>Grace-Mar digest</h1><p>Generated " + data["generated_at"][:10] + "</p>"
    if data.get("entries"):
        body += "<h2>Journal highlights</h2><ul>"
        for e in data["entries"]:
            body += f"<li><strong>{e['date']}</strong> — {e['entry']}</li>"
        body += "</ul>"
    if data.get("curiosity"):
        body += "<h2>Curiosity</h2><ul>"
        for t in data["curiosity"]:
            body += f"<li>{t}</li>"
        body += "</ul>"
    return f"<!DOCTYPE html><html><head><meta charset='utf-8'><title>Digest</title></head><body>{body}</body></html>"


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate newsletter digest from journal + curiosity")
    parser.add_argument("--user", "-u", default="grace-mar", help="User id")
    parser.add_argument("--output", "-o", default=None, help="Output file (default: stdout)")
    parser.add_argument("--format", "-f", choices=("md", "html"), default="md", help="Output format")
    parser.add_argument("--days", type=int, default=7, help="Include journal entries from last N days")
    parser.add_argument("--no-curiosity", action="store_true", help="Omit IX-B curiosity section")
    args = parser.parse_args()
    data = build_digest(user_id=args.user, days=args.days, include_curiosity=not args.no_curiosity)
    text = render_markdown(data) if args.format == "md" else render_html(data)
    if args.output:
        out_path = Path(args.output)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(text, encoding="utf-8")
        print(f"Wrote {args.output}", file=__import__("sys").stderr)
    else:
        print(text)


if __name__ == "__main__":
    main()

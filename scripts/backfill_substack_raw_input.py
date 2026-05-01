#!/usr/bin/env python3
"""Backfill a Substack publication year into strategy-notebook raw-input/.

Uses the public JSON API (no API key):
  GET https://{hostname}/api/v1/archive?sort=new&offset=N&limit=50
  GET https://{hostname}/api/v1/posts/{slug}

Writes one markdown file per post with YAML frontmatter (optional ``thread:``),
body as HTML-stripped plain text (full HTML is large; canonical URL in frontmatter).
Treat the archive as a discovery index, not a completeness mandate: the caller
still chooses which substantial posts merit preservation in raw-input/.

WORK only; not Record.

Example::

  python3 scripts/backfill_substack_raw_input.py \\
    --hostname simplicius76.substack.com --year 2026 --thread simplicius --apply
"""

from __future__ import annotations

import argparse
import json
import re
import textwrap
import urllib.error
import urllib.request
from datetime import date, datetime, timezone
from html import unescape
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_RAW_ROOT = (
    REPO_ROOT / "docs/skill-work/work-strategy/strategy-notebook/raw-input"
)
USER_AGENT = "grace-mar-backfill-substack/1.0 (+local strategy notebook)"

# Reuse HTML stripping from fetch_strategy_raw_input
import sys

sys.path.insert(0, str(REPO_ROOT / "scripts"))
from fetch_strategy_raw_input import _slugify  # noqa: E402


def _strip_html(html: str) -> str:
    if not html:
        return ""
    text = re.sub(r"(?is)<script[^>]*>.*?</script>", " ", html)
    text = re.sub(r"(?is)<style[^>]*>.*?</style>", " ", text)
    text = re.sub(r"<br\s*/?>", "\n", text, flags=re.I)
    text = re.sub(r"</p\s*>", "\n\n", text, flags=re.I)
    text = re.sub(r"<[^>]+>", " ", text)
    text = unescape(text)
    text = re.sub(r"[ \t\r\f\v]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text).strip()
    return text


def _fetch_json(url: str, *, timeout: int = 60) -> object:
    req = urllib.request.Request(
        url,
        headers={"User-Agent": USER_AGENT, "Accept": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))


def _post_day_utc(iso_z: str) -> date:
    if iso_z.endswith("Z"):
        iso_z = iso_z[:-1] + "+00:00"
    dt = datetime.fromisoformat(iso_z)
    if dt.tzinfo is not None:
        dt = dt.astimezone(timezone.utc)
    return dt.date()


def _build_doc(
    *,
    post: dict,
    body_text: str,
    ingest_date: date,
    thread: str | None,
    publication_host: str,
) -> str:
    day = _post_day_utc(post["post_date"])
    title = post.get("title") or post.get("slug") or "untitled"
    canonical = post.get("canonical_url") or f"https://{publication_host}/p/{post['slug']}"
    front = {
        "ingest_date": ingest_date.isoformat(),
        "pub_date": day.isoformat(),
        "kind": "substack-post",
        "source_url": canonical,
        "publication": publication_host,
        "slug": post["slug"],
        "post_id": post.get("id"),
    }
    if thread:
        front["thread"] = thread
    yaml_lines = ["---"]
    for k, v in front.items():
        if v is None:
            continue
        yaml_lines.append(f"{k}: {v}")
    yaml_lines.append("---")
    teaser = (post.get("description") or post.get("subtitle") or "").strip()
    parts = [
        "\n".join(yaml_lines),
        "",
        f"# {title}",
        "",
        f"**Canonical:** {canonical}",
        "",
    ]
    if teaser:
        parts.extend(["## Teaser (API)", "", teaser, ""])
    parts.extend(
        [
            "## Body (plain text, HTML stripped)",
            "",
            textwrap.fill(_strip_html(body_text), width=92) if body_text else "_(empty)_",
            "",
            f"_Backfill: `scripts/backfill_substack_raw_input.py`; not Record._",
            "",
        ]
    )
    return "\n".join(parts)


def run(
    *,
    hostname: str,
    year: int,
    raw_root: Path,
    ingest_date: date,
    thread: str | None,
    apply: bool,
    limit: int,
) -> int:
    raw_root = raw_root.resolve()
    collected: list[dict] = []
    offset = 0
    host = hostname.strip().rstrip("/")
    if host.startswith("https://"):
        host = host[len("https://") :]

    while True:
        url = f"https://{host}/api/v1/archive?sort=new&offset={offset}&limit={limit}"
        try:
            batch = _fetch_json(url)
        except (urllib.error.URLError, json.JSONDecodeError, TimeoutError) as e:
            print(f"ERROR archive offset={offset}: {e}")
            break
        if not isinstance(batch, list) or not batch:
            break
        for item in batch:
            if not isinstance(item, dict):
                continue
            try:
                d = _post_day_utc(item["post_date"])
            except (KeyError, ValueError):
                continue
            if d.year == year:
                collected.append(item)
        if all(_post_day_utc(x["post_date"]) < date(year, 1, 1) for x in batch if "post_date" in x):
            break
        offset += len(batch)

    # Dedupe by slug, sort by date
    by_slug: dict[str, dict] = {}
    for item in collected:
        by_slug[item["slug"]] = item
    ordered = sorted(by_slug.values(), key=lambda x: x["post_date"])

    print(f"Found {len(ordered)} post(s) in {year} for {host}")

    for post in ordered:
        slug = post["slug"]
        post_url = f"https://{host}/api/v1/posts/{slug}"
        try:
            detail = _fetch_json(post_url)
        except (urllib.error.URLError, json.JSONDecodeError, TimeoutError) as e:
            print(f"  skip {slug}: {e}")
            continue
        if not isinstance(detail, dict):
            continue
        body_html = detail.get("body_html") or ""
        day = _post_day_utc(post["post_date"])
        fname = f"substack-simplicius-{_slugify(slug, max_len=60)}-{day.isoformat()}.md"
        dest = raw_root / day.isoformat() / fname
        content = _build_doc(
            post=detail,
            body_text=body_html,
            ingest_date=ingest_date,
            thread=thread,
            publication_host=host,
        )
        rel = dest.relative_to(REPO_ROOT)
        if dest.is_file() and dest.read_text(encoding="utf-8") == content:
            print(f"  skip unchanged: {rel}")
            continue
        if not apply:
            print(f"  would write: {rel}")
            continue
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(content, encoding="utf-8")
        print(f"  wrote: {rel}")

    if not apply and ordered:
        print("\nDry-run only. Pass --apply to write files.")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--hostname", default="simplicius76.substack.com", help="Substack host")
    ap.add_argument("--year", type=int, default=2026)
    ap.add_argument("--root", type=Path, default=DEFAULT_RAW_ROOT)
    ap.add_argument("--ingest-date", type=str, default=None, help="YYYY-MM-DD ingest_date in frontmatter")
    ap.add_argument("--thread", type=str, default=None, help="expert_id for YAML thread: (e.g. simplicius)")
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--limit", type=int, default=30, help="archive page size")
    args = ap.parse_args()

    ingest = (
        datetime.strptime(args.ingest_date, "%Y-%m-%d").date()
        if args.ingest_date
        else date.today()
    )

    return run(
        hostname=args.hostname,
        year=args.year,
        raw_root=args.root,
        ingest_date=ingest,
        thread=args.thread,
        apply=args.apply,
        limit=max(1, min(args.limit, 50)),
    )


if __name__ == "__main__":
    raise SystemExit(main())

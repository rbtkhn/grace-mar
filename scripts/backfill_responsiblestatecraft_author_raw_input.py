#!/usr/bin/env python3
"""Backfill Responsible Statecraft author-page articles into raw-input/.

This is a best-effort public archive importer:

1. Crawl a public author page for visible article links.
2. Fetch each linked article page and extract title, date, and body text.
3. Write one markdown file per article under ``raw-input/<pub_date>/``.

WORK only; not Record.

Example::

  python3 scripts/backfill_responsiblestatecraft_author_raw_input.py --apply \
    --author-url https://responsiblestatecraft.org/author/tparsi/ --thread parsi
"""

from __future__ import annotations

import argparse
import re
import sys
import textwrap
import urllib.error
import urllib.request
from datetime import date, datetime, timezone
from html import unescape
from pathlib import Path
from typing import Iterable
from urllib.parse import urljoin, urlparse

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_RAW_ROOT = (
    REPO_ROOT / "docs/skill-work/work-strategy/strategy-notebook/raw-input"
)
DEFAULT_AUTHOR_URL = "https://responsiblestatecraft.org/author/tparsi/"
USER_AGENT = (
    "grace-mar-backfill-responsible-statecraft/1.0 "
    "(+local strategy notebook ingest)"
)

import sys as _sys

if str(REPO_ROOT / "scripts") not in _sys.path:
    _sys.path.insert(0, str(REPO_ROOT / "scripts"))

from fetch_strategy_raw_input import _slugify  # noqa: E402
from strategy_expert_transcript import iter_raw_input_yaml_documents  # noqa: E402

_META_RE_TEMPLATE = (
    r'<meta[^>]+(?:property|name)=["\']{name}["\'][^>]+content=(?P<quote>["\'])'
    r'(?P<content>.*?)(?P=quote)'
)

_ARTICLE_EXCLUDE = {
    "author",
    "about",
    "about-us",
    "contact",
    "privacy-policy",
    "editorial-and-submission-policy",
    "video-section",
    "analysis",
    "media",
    "military-industrial-complex",
    "washington-politics",
    "global-crises",
    "north-america",
    "europe",
    "asia-pacific",
    "africa",
    "latin-america",
}


def _fetch_html(url: str, *, timeout: int = 45) -> str:
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": USER_AGENT,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        },
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        charset = resp.headers.get_content_charset() or "utf-8"
        return resp.read().decode(charset, errors="replace")


def _author_handle(author_url: str) -> str:
    parsed = urlparse(author_url)
    parts = [p for p in parsed.path.split("/") if p]
    if not parts:
        raise ValueError(f"Could not infer author slug from URL: {author_url}")
    return parts[-1].lstrip("@")


def _normalize_url(raw_url: str, *, base_url: str) -> str | None:
    abs_url = urljoin(base_url, raw_url.strip())
    parsed = urlparse(abs_url)
    if parsed.scheme not in {"http", "https"}:
        return None
    netloc = parsed.netloc.lower()
    if netloc.startswith("www."):
        netloc = netloc[4:]
    if netloc != "responsiblestatecraft.org":
        return None
    path = parsed.path or "/"
    if path.endswith("/"):
        path = path[:-1]
    parts = [p for p in path.split("/") if p]
    if len(parts) != 1:
        return None
    slug = parts[0].lower()
    if slug in _ARTICLE_EXCLUDE or not re.search(r"[a-z].*-[a-z]", slug):
        return None
    return f"https://responsiblestatecraft.org/{parts[0].strip('/')}/"


def _extract_article_urls(author_html: str, author_url: str) -> list[str]:
    urls: list[str] = []
    seen: set[str] = set()
    for m in re.finditer(r'href=["\']([^"\']+)["\']', author_html, re.I):
        raw = m.group(1).strip()
        abs_url = _normalize_url(raw, base_url=author_url)
        if not abs_url or abs_url in seen:
            continue
        seen.add(abs_url)
        urls.append(abs_url)
    return urls


def _first_meta_content(html: str, *, name: str) -> str | None:
    tag_pattern = re.compile(
        _META_RE_TEMPLATE.format(name=re.escape(name)),
        re.I | re.S,
    )
    m = tag_pattern.search(html)
    if not m:
        return None
    tag = m.group(0)
    m2 = re.search(r'content=(["\'])(?P<content>.*?)\1', tag, re.I | re.S)
    if not m2:
        return None
    return unescape(m2.group("content").strip())


def _extract_datetime(html: str) -> datetime | None:
    for name in ("article:published_time", "article:modified_time", "og:updated_time"):
        published = _first_meta_content(html, name=name)
        if published:
            try:
                iso = published[:-1] + "+00:00" if published.endswith("Z") else published
                dt = datetime.fromisoformat(iso)
                if dt.tzinfo is not None:
                    dt = dt.astimezone(timezone.utc)
                return dt
            except ValueError:
                pass
    m = re.search(r'<time[^>]+datetime=["\']([^"\']+)["\']', html, re.I)
    if m:
        raw = m.group(1).strip()
        try:
            iso = raw[:-1] + "+00:00" if raw.endswith("Z") else raw
            dt = datetime.fromisoformat(iso)
            if dt.tzinfo is not None:
                dt = dt.astimezone(timezone.utc)
            return dt
        except ValueError:
            return None
    return None


def _extract_title(html: str) -> str:
    for name in ("og:title", "twitter:title", "title"):
        text = _first_meta_content(html, name=name)
        if text:
            return text.strip()
    m = re.search(r"<h1[^>]*>(?P<body>.*?)</h1>", html, re.I | re.S)
    if m:
        return _clean_text(m.group("body")).strip()
    return "untitled"


def _clean_text(text: str) -> str:
    text = unescape(text)
    text = re.sub(r"(?is)<script[^>]*>.*?</script>", " ", text)
    text = re.sub(r"(?is)<style[^>]*>.*?</style>", " ", text)
    text = re.sub(r"<br\s*/?>", "\n", text, flags=re.I)
    text = re.sub(r"</p\s*>", "\n\n", text, flags=re.I)
    text = re.sub(r"</div\s*>", "\n", text, flags=re.I)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"[ \t\r\f\v]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def _extract_article_body(html: str, title: str) -> str:
    for pattern in (
        r"(?is)<article\b[^>]*>(?P<body>.*?)</article>",
        r"(?is)<main\b[^>]*>(?P<body>.*?)</main>",
    ):
        m = re.search(pattern, html)
        if m:
            body = _clean_text(m.group("body"))
            if body:
                break
    else:
        body = _clean_text(html)

    paras = [p.strip() for p in re.split(r"\n\s*\n", body) if p.strip()]
    if paras and paras[0] == title:
        paras = paras[1:]
    elif paras and paras[0].startswith(title):
        paras[0] = paras[0][len(title) :].lstrip(" -:—")
    if paras and re.fullmatch(r"(Trita Parsi|Responsible Statecraft)", paras[0]):
        paras = paras[1:]
    return "\n\n".join(paras).strip()


def _source_urls_in_raw_input(raw_root: Path) -> set[str]:
    out: set[str] = set()
    if not raw_root.is_dir():
        return out
    for md in raw_root.rglob("*.md"):
        try:
            text = md.read_text(encoding="utf-8")
        except OSError:
            continue
        for fm, _body in iter_raw_input_yaml_documents(text):
            src = (fm.get("source_url") or "").strip()
            if src:
                out.add(src)
    return out


def _build_doc(
    *,
    author: str,
    author_url: str,
    article_url: str,
    slug: str,
    ingest_date: date,
    pub_date: date,
    title: str,
    body_text: str,
    thread: str | None,
) -> str:
    front = {
        "ingest_date": ingest_date.isoformat(),
        "pub_date": pub_date.isoformat(),
        "kind": "rss-item",
        "account_author": author,
        "source_url_profile": author_url,
        "source_url": article_url,
        "publication": "responsiblestatecraft.org",
        "slug": slug,
    }
    if thread:
        front["thread"] = thread
    yaml_lines = ["---"]
    for k, v in front.items():
        if v is None:
            continue
        yaml_lines.append(f"{k}: {v}")
    yaml_lines.append("---")
    parts = [
        "\n".join(yaml_lines),
        "",
        f"# {title}",
        "",
        f"**Canonical:** {article_url}",
        f"**Author page:** {author_url}",
        f"**Published:** {pub_date.isoformat()}",
        "",
        "## Article text",
        "",
        textwrap.fill(body_text or "_(empty)_", width=92) if body_text else "_(empty)_",
        "",
        "_Backfill: `scripts/backfill_responsiblestatecraft_author_raw_input.py`; not Record._",
        "",
    ]
    return "\n".join(parts)


def _normalize_article_urls(urls: Iterable[str]) -> list[str]:
    out: list[str] = []
    seen: set[str] = set()
    for url in urls:
        url = url.strip()
        if not url:
            continue
        norm = _normalize_url(url, base_url="https://responsiblestatecraft.org/")
        if not norm or norm in seen:
            continue
        seen.add(norm)
        out.append(norm)
    return out


def run(
    *,
    author_url: str,
    raw_root: Path,
    ingest_date: date,
    thread: str | None,
    apply: bool,
    limit: int,
    article_urls: list[str] | None = None,
) -> int:
    raw_root = raw_root.resolve()
    author = _author_handle(author_url)
    discovered: list[str] = []
    if article_urls:
        discovered.extend(article_urls)
    else:
        try:
            author_html = _fetch_html(author_url)
            discovered.extend(_extract_article_urls(author_html, author_url))
        except (urllib.error.URLError, TimeoutError, ValueError) as e:
            print(f"ERROR author crawl: {e}")
    discovered = _normalize_article_urls(discovered)
    if limit > 0:
        discovered = discovered[:limit]
    if not discovered:
        print(f"No article URLs found for {author_url}")
        return 0

    seen_source_urls = _source_urls_in_raw_input(raw_root)
    print(f"Found {len(discovered)} article URL(s) for @{author}")

    for article_url in discovered:
        if article_url in seen_source_urls:
            print(f"  skip existing source_url: {article_url}")
            continue
        slug = article_url.rstrip("/").rsplit("/", 1)[-1]
        try:
            html = _fetch_html(article_url)
        except (urllib.error.URLError, TimeoutError) as e:
            print(f"  skip {slug}: {e}")
            continue
        title = _extract_title(html)
        dt = _extract_datetime(html)
        pub_day = dt.date() if dt else ingest_date
        body_text = _extract_article_body(html, title)
        dest = raw_root / pub_day.isoformat() / (
            f"rs-{_slugify(author, max_len=24)}-{_slugify(slug, max_len=60)}-{pub_day.isoformat()}.md"
        )
        content = _build_doc(
            author=f"@{author}",
            author_url=author_url,
            article_url=article_url,
            slug=slug,
            ingest_date=ingest_date,
            pub_date=pub_day,
            title=title,
            body_text=body_text,
            thread=thread,
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
        seen_source_urls.add(article_url)

    if not apply:
        print("\nDry-run only. Pass --apply to write files.")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--author-url",
        default=DEFAULT_AUTHOR_URL,
        help="Responsible Statecraft author page URL",
    )
    ap.add_argument("--root", type=Path, default=DEFAULT_RAW_ROOT)
    ap.add_argument("--ingest-date", type=str, default=None, help="YYYY-MM-DD ingest_date in frontmatter")
    ap.add_argument("--thread", type=str, default=None, help="expert_id for YAML thread: (e.g. parsi)")
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--limit", type=int, default=20, help="Max article URLs to process")
    ap.add_argument(
        "--article-url",
        action="append",
        dest="article_urls",
        default=None,
        help="Explicit article URL to backfill (repeatable)",
    )
    args = ap.parse_args()

    ingest = (
        datetime.strptime(args.ingest_date, "%Y-%m-%d").date()
        if args.ingest_date
        else date.today()
    )

    return run(
        author_url=args.author_url,
        raw_root=args.root,
        ingest_date=ingest,
        thread=args.thread,
        apply=args.apply,
        limit=max(1, min(args.limit, 100)),
        article_urls=args.article_urls or None,
    )


if __name__ == "__main__":
    raise SystemExit(main())

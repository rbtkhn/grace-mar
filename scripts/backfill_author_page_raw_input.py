#!/usr/bin/env python3
"""Backfill a public author page into strategy-notebook raw-input/.

Generic best-effort public archive importer:

1. Crawl a public author page for visible article links.
2. Fetch each linked article page and extract title, date, and body text.
3. Write one markdown file per article under ``raw-input/<pub_date>/``.

The caller supplies the target domain plus a path-shape hint so the same
helper can serve multiple public author/archive surfaces.

WORK only; not Record.
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
USER_AGENT = "grace-mar-backfill-author-page/1.0 (+local strategy notebook ingest)"

import sys as _sys

if str(REPO_ROOT / "scripts") not in _sys.path:
    _sys.path.insert(0, str(REPO_ROOT / "scripts"))

from fetch_strategy_raw_input import _slugify  # noqa: E402
from strategy_expert_transcript import iter_raw_input_yaml_documents  # noqa: E402

_META_RE_TEMPLATE = (
    r'<meta[^>]+(?:property|name)=["\']{name}["\'][^>]+content=(?P<quote>["\'])'
    r'(?P<content>.*?)(?P=quote)'
)


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
        paras[0] = paras[0][len(title) :].lstrip(" -:â€”")
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


def _path_matches_shape(path: str, shape: str, *, domain: str) -> bool:
    parts = [p for p in path.split("/") if p]
    if shape == "single-segment":
        return len(parts) == 1
    if shape == "date-slug":
        return len(parts) >= 4 and all(re.fullmatch(r"\d{4}", parts[i]) or re.fullmatch(r"\d{2}", parts[i]) for i in range(3))
    if shape == "any-article":
        return len(parts) >= 1
    raise ValueError(f"Unknown path shape: {shape}")


def _normalize_url(
    raw_url: str,
    *,
    base_url: str,
    domain: str,
    path_shape: str,
    exclude_prefixes: Iterable[str],
) -> str | None:
    abs_url = urljoin(base_url, raw_url.strip())
    parsed = urlparse(abs_url)
    if parsed.scheme not in {"http", "https"}:
        return None
    netloc = parsed.netloc.lower()
    if netloc.startswith("www."):
        netloc = netloc[4:]
    domain = domain.lower().lstrip("www.")
    if netloc != domain:
        return None
    path = parsed.path or "/"
    if path.endswith("/"):
        path = path[:-1]
    parts = [p for p in path.split("/") if p]
    if not parts:
        return None
    if any(parts[0].lower() == ex.lower().strip("/") for ex in exclude_prefixes):
        return None
    if not _path_matches_shape(path, path_shape, domain=domain):
        return None
    return f"https://{domain}/{path.lstrip('/')}/"


def _extract_article_urls(
    author_html: str,
    author_url: str,
    *,
    domain: str,
    path_shape: str,
    exclude_prefixes: Iterable[str],
) -> list[str]:
    urls: list[str] = []
    seen: set[str] = set()
    for m in re.finditer(r'href=["\']([^"\']+)["\']', author_html, re.I):
        raw = m.group(1).strip()
        abs_url = _normalize_url(
            raw,
            base_url=author_url,
            domain=domain,
            path_shape=path_shape,
            exclude_prefixes=exclude_prefixes,
        )
        if not abs_url or abs_url in seen:
            continue
        seen.add(abs_url)
        urls.append(abs_url)
    return urls


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
    publication: str,
) -> str:
    front = {
        "ingest_date": ingest_date.isoformat(),
        "pub_date": pub_date.isoformat(),
        "kind": "rss-item",
        "account_author": author,
        "source_url_profile": author_url,
        "source_url": article_url,
        "publication": publication,
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
        "",
        "## Body (plain text, HTML stripped)",
        "",
        textwrap.fill(body_text or "_(empty)_", width=92) if body_text else "_(empty)_",
        "",
        f"_Backfill: `scripts/backfill_author_page_raw_input.py`; not Record._",
        "",
    ]
    return "\n".join(parts)


def run(
    *,
    author_url: str,
    domain: str,
    path_shape: str,
    publication: str,
    raw_root: Path,
    ingest_date: date,
    thread: str | None,
    apply: bool,
    limit: int,
    exclude_prefixes: list[str] | None = None,
) -> int:
    raw_root = raw_root.resolve()
    author_html = _fetch_html(author_url)
    article_urls = _extract_article_urls(
        author_html,
        author_url,
        domain=domain,
        path_shape=path_shape,
        exclude_prefixes=exclude_prefixes or [],
    )
    seen_sources = _source_urls_in_raw_input(raw_root)
    author = _author_handle(author_url)
    print(f"Found {len(article_urls)} candidate article link(s) at {author_url}")

    count = 0
    for article_url in article_urls:
        if article_url in seen_sources:
            print(f"  skip existing: {article_url}")
            continue
        if count >= limit:
            break
        try:
            html = _fetch_html(article_url)
        except (urllib.error.URLError, TimeoutError) as e:
            print(f"  skip {article_url}: {e}")
            continue
        dt = _extract_datetime(html)
        if not dt:
            print(f"  skip {article_url}: could not determine publication date")
            continue
        title = _extract_title(html)
        body = _extract_article_body(html, title)
        slug = article_url.rstrip("/").split("/")[-1]
        day = dt.date()
        fname = f"{_slugify(slug, max_len=60)}-{day.isoformat()}.md"
        dest = raw_root / day.isoformat() / fname
        content = _build_doc(
            author=author,
            author_url=author_url,
            article_url=article_url,
            slug=slug,
            ingest_date=ingest_date,
            pub_date=day,
            title=title,
            body_text=body,
            thread=thread,
            publication=publication,
        )
        rel = dest.relative_to(REPO_ROOT)
        if dest.is_file() and dest.read_text(encoding="utf-8") == content:
            print(f"  skip unchanged: {rel}")
            continue
        if not apply:
            print(f"  would write: {rel}")
            count += 1
            continue
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(content, encoding="utf-8")
        print(f"  wrote: {rel}")
        count += 1

    if not apply and article_urls:
        print("\nDry-run only. Pass --apply to write files.")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--author-url", required=True)
    ap.add_argument("--domain", required=True)
    ap.add_argument("--path-shape", choices=["single-segment", "date-slug", "any-article"], default="single-segment")
    ap.add_argument("--publication", required=True)
    ap.add_argument("--root", type=Path, default=DEFAULT_RAW_ROOT)
    ap.add_argument("--ingest-date", type=str, default=None, help="YYYY-MM-DD ingest_date in frontmatter")
    ap.add_argument("--thread", type=str, default=None)
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--limit", type=int, default=50)
    ap.add_argument("--exclude-prefix", action="append", default=[])
    args = ap.parse_args()

    ingest = (
        datetime.strptime(args.ingest_date, "%Y-%m-%d").date()
        if args.ingest_date
        else date.today()
    )

    return run(
        author_url=args.author_url,
        domain=args.domain,
        path_shape=args.path_shape,
        publication=args.publication,
        raw_root=args.root,
        ingest_date=ingest,
        thread=args.thread,
        apply=args.apply,
        limit=max(1, min(args.limit, 100)),
        exclude_prefixes=args.exclude_prefix,
    )


if __name__ == "__main__":
    raise SystemExit(main())

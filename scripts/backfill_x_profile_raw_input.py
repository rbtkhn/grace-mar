#!/usr/bin/env python3
"""Backfill X profile/status posts into strategy-notebook raw-input/.

This is a best-effort public-profile importer:

1. Crawl a public X profile page for visible ``/status/<id>`` links.
2. Fetch each status page and extract post text plus published time.
3. Write one ``kind: x-post-text`` markdown file per post under
   ``raw-input/<pub_date>/``.

The script is intentionally conservative:
- It does not require or manage login cookies.
- It skips files whose ``source_url`` already exists in raw-input/.
- It falls back to an explicit ``--status-url`` list if profile crawl returns
  nothing or if you want to seed a specific set of posts.

WORK only; not Record.

Example::

  python3 scripts/backfill_x_profile_raw_input.py --apply \
    --profile-url https://x.com/RealScottRitter --thread ritter
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
from urllib.parse import urlparse

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_RAW_ROOT = (
    REPO_ROOT / "docs/skill-work/work-strategy/strategy-notebook/raw-input"
)
DEFAULT_PROFILE_URL = "https://x.com/RealScottRitter"
USER_AGENT = (
    "grace-mar-backfill-x-profile/1.0 "
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


def _profile_handle(profile_url: str) -> str:
    parsed = urlparse(profile_url)
    parts = [p for p in parsed.path.split("/") if p]
    if not parts:
        raise ValueError(f"Could not infer X handle from profile URL: {profile_url}")
    return parts[-1].lstrip("@")


def _extract_status_urls(profile_html: str, handle: str) -> list[str]:
    urls: list[str] = []
    seen: set[str] = set()
    pattern = re.compile(
        rf'(?:https?://(?:www\.)?x\.com/{re.escape(handle)}/status/\d+|/{re.escape(handle)}/status/\d+)'
    )
    for match in pattern.finditer(profile_html):
        raw = match.group(0)
        if raw.startswith("/"):
            raw = f"https://x.com{raw}"
        raw = raw.replace("www.x.com", "x.com")
        if raw in seen:
            continue
        seen.add(raw)
        urls.append(raw)
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


def _extract_status_datetime(html: str) -> datetime | None:
    published = _first_meta_content(html, name="article:published_time")
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
    if not m:
        return None
    raw = m.group(1).strip()
    try:
        iso = raw[:-1] + "+00:00" if raw.endswith("Z") else raw
        dt = datetime.fromisoformat(iso)
        if dt.tzinfo is not None:
            dt = dt.astimezone(timezone.utc)
        return dt
    except ValueError:
        return None


def _clean_text(text: str) -> str:
    text = unescape(text)
    text = re.sub(r"<br\s*/?>", "\n", text, flags=re.I)
    text = re.sub(r"</p\s*>", "\n\n", text, flags=re.I)
    text = re.sub(r"</div\s*>", "\n", text, flags=re.I)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"[ \t\r\f\v]+", " ", text)
    text = re.sub(r" *\n *", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def _extract_status_text(html: str) -> str:
    # Prefer the main tweet text block when present.
    m = re.search(
        r'data-testid=["\']tweetText["\'][^>]*>(?P<body>.*?)</div>',
        html,
        re.I | re.S,
    )
    if m:
        text = _clean_text(m.group("body"))
        if text:
            return text

    for meta_name in ("og:description", "twitter:description", "description"):
        text = _first_meta_content(html, name=meta_name)
        if text:
            text = re.sub(r"^.+?\bon X:\s*", "", text, flags=re.I)
            return text.strip()
    return ""


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
    handle: str,
    profile_url: str,
    status_url: str,
    ingest_date: date,
    pub_date: date,
    status_id: str,
    text: str,
    thread: str | None,
) -> str:
    front = {
        "ingest_date": ingest_date.isoformat(),
        "pub_date": pub_date.isoformat(),
        "kind": "x-post-text",
        "account_author": f"@{handle}",
        "source_url_profile": profile_url,
        "source_url": status_url,
        "status_id": status_id,
    }
    if thread:
        front["thread"] = thread
    yaml_lines = ["---"]
    for k, v in front.items():
        if v is None:
            continue
        yaml_lines.append(f"{k}: {v}")
    yaml_lines.append("---")
    title = f"@{handle} Post"
    parts = [
        "\n".join(yaml_lines),
        "",
        f"# {title}",
        "",
        f"**Status:** {status_url}",
        f"**Published:** {pub_date.isoformat()}",
        "",
        "## Post text",
        "",
        textwrap.fill(text or "_(empty)_", width=92) if text else "_(empty)_",
        "",
        "_Backfill: `scripts/backfill_x_profile_raw_input.py`; not Record._",
        "",
    ]
    return "\n".join(parts)


def _normalize_status_urls(urls: Iterable[str]) -> list[str]:
    out: list[str] = []
    seen: set[str] = set()
    for url in urls:
        url = url.strip()
        if not url:
            continue
        url = url.replace("www.x.com", "x.com")
        if url in seen:
            continue
        seen.add(url)
        out.append(url)
    return out


def run(
    *,
    profile_url: str,
    raw_root: Path,
    ingest_date: date,
    thread: str | None,
    apply: bool,
    limit: int,
    status_urls: list[str] | None = None,
) -> int:
    raw_root = raw_root.resolve()
    handle = _profile_handle(profile_url)
    discovered: list[str] = []
    if status_urls:
        discovered.extend(status_urls)
    else:
        try:
            profile_html = _fetch_html(profile_url)
            discovered.extend(_extract_status_urls(profile_html, handle))
        except (urllib.error.URLError, TimeoutError, ValueError) as e:
            print(f"ERROR profile crawl: {e}")

    discovered = _normalize_status_urls(discovered)
    if limit > 0:
        discovered = discovered[:limit]

    if not discovered:
        print(f"No status URLs found for {profile_url}")
        return 0

    seen_source_urls = _source_urls_in_raw_input(raw_root)
    print(f"Found {len(discovered)} status URL(s) for {handle}")

    for status_url in discovered:
        if status_url in seen_source_urls:
            print(f"  skip existing source_url: {status_url}")
            continue
        status_id = status_url.rsplit("/", 1)[-1]
        try:
            html = _fetch_html(status_url)
        except (urllib.error.URLError, TimeoutError) as e:
            print(f"  skip {status_id}: {e}")
            continue
        text = _extract_status_text(html)
        dt = _extract_status_datetime(html)
        pub_day = dt.date() if dt else ingest_date
        dest = raw_root / pub_day.isoformat() / (
            f"x-{_slugify(handle, max_len=24)}-{status_id}-{pub_day.isoformat()}.md"
        )
        content = _build_doc(
            handle=handle,
            profile_url=profile_url,
            status_url=status_url,
            ingest_date=ingest_date,
            pub_date=pub_day,
            status_id=status_id,
            text=text,
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
        seen_source_urls.add(status_url)

    if not apply:
        print("\nDry-run only. Pass --apply to write files.")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--profile-url", default=DEFAULT_PROFILE_URL)
    ap.add_argument("--root", type=Path, default=DEFAULT_RAW_ROOT)
    ap.add_argument("--ingest-date", type=str, default=None)
    ap.add_argument("--thread", type=str, default="ritter")
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--limit", type=int, default=25)
    ap.add_argument(
        "--status-url",
        action="append",
        default=[],
        help="Explicit X status URL; may be repeated. If provided, profile crawl is skipped.",
    )
    args = ap.parse_args()

    ingest = (
        datetime.strptime(args.ingest_date, "%Y-%m-%d").date()
        if args.ingest_date
        else date.today()
    )
    status_urls = _normalize_status_urls(args.status_url)
    return run(
        profile_url=args.profile_url,
        raw_root=args.root,
        ingest_date=ingest,
        thread=args.thread,
        apply=args.apply,
        limit=max(1, args.limit),
        status_urls=status_urls if status_urls else None,
    )


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Fetch external sources into strategy-notebook raw-input/ (network pull).

Fills the gap left by ``populate_strategy_raw_input.py``, which only **mirrors**
artifacts already on disk (transcripts, verbatim sidecars, screenshot indexes).

Supported source kinds (extend over time):
  - ``rss`` — RSS 2.0 and Atom feeds (Substack, many blogs, news sites)

Config: JSON next to raw-input (see ``fetch-sources.example.json``).
Each feed may set optional ``"thread": "<expert_id>"`` (must match
``CANONICAL_EXPERT_IDS``); written into YAML so ``strategy_thread.py`` triage
can merge ``kind: rss-item`` rows into that expert's transcript.

Override path with ``FETCH_STRATEGY_SOURCES`` env or ``--config``.

WORK only; not Record. Network use is explicit (--apply).

Usage::
  python3 scripts/fetch_strategy_raw_input.py --dry-run
  python3 scripts/fetch_strategy_raw_input.py --apply
  python3 scripts/fetch_strategy_raw_input.py --apply --today 2026-04-25
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import textwrap
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from datetime import date, datetime, timezone
from email.utils import parsedate_to_datetime
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

REPO_ROOT = Path(__file__).resolve().parent.parent
_SCRIPTS = REPO_ROOT / "scripts"
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from strategy_expert_corpus import _EXPERT_IDS_SET  # noqa: E402
DEFAULT_NOTEBOOK = REPO_ROOT / "docs/skill-work/work-strategy/strategy-notebook"
DEFAULT_RAW_ROOT = DEFAULT_NOTEBOOK / "raw-input"
DEFAULT_CONFIG = DEFAULT_RAW_ROOT / "fetch-sources.json"
USER_AGENT = (
    "grace-mar-fetch-strategy-raw-input/1.0 "
    "(+https://github.com/grace-mar; local strategy notebook ingest)"
)


def _slugify(s: str, max_len: int = 48) -> str:
    s = s.lower().strip()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    s = re.sub(r"-+", "-", s).strip("-")
    return s[:max_len].rstrip("-") or "item"


def _strip_html(html: str) -> str:
    if not html:
        return ""
    text = re.sub(r"(?is)<script[^>]*>.*?</script>", " ", html)
    text = re.sub(r"(?is)<style[^>]*>.*?</style>", " ", text)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def _fetch_url(url: str, *, timeout: int = 45) -> bytes:
    req = urllib.request.Request(
        url,
        headers={"User-Agent": USER_AGENT, "Accept": "application/rss+xml, application/atom+xml, text/xml, */*"},
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read()


def _local_tag(tag: str) -> str:
    return tag.rpartition("}")[2] or tag


def _parse_pub_date(text: str | None) -> date | None:
    if not text:
        return None
    text = text.strip()
    try:
        dt = parsedate_to_datetime(text)
        if dt.tzinfo is not None:
            dt = dt.astimezone(timezone.utc)
        return dt.date()
    except (TypeError, ValueError, OverflowError):
        pass
    if text.endswith("Z"):
        iso = text[:-1] + "+00:00"
    else:
        iso = text
    try:
        dt = datetime.fromisoformat(iso)
        if dt.tzinfo is not None:
            dt = dt.astimezone(timezone.utc)
        return dt.date()
    except ValueError:
        pass
    if len(text) >= 10 and text[4] == "-" and text[7] == "-":
        try:
            return datetime.strptime(text[:10], "%Y-%m-%d").date()
        except ValueError:
            pass
    return None


def _iter_rss_items(root: ET.Element) -> list[dict[str, str | None]]:
    """Return list of dicts: title, link, pub_raw, summary_html, guid."""
    tag = root.tag
    if tag.endswith("}rss") or tag == "rss":
        channel = root.find("channel")
        if channel is None:
            return []
        out: list[dict[str, str | None]] = []
        for item in channel.findall("item"):
            title_el = item.find("title")
            link_el = item.find("link")
            pub_el = item.find("pubDate")
            guid_el = item.find("guid")
            desc_el = item.find("description")
            enc_el = item.find("{http://purl.org/rss/1.0/modules/content/}encoded")
            title = (title_el.text or "").strip() if title_el is not None else ""
            link = (link_el.text or "").strip() if link_el is not None else ""
            pub = (pub_el.text or "").strip() if pub_el is not None else None
            guid = (guid_el.text or "").strip() if guid_el is not None else None
            body = None
            if enc_el is not None and (enc_el.text or enc_el.tail):
                body = (enc_el.text or "") + (enc_el.tail or "")
            elif desc_el is not None and desc_el.text:
                body = desc_el.text
            out.append(
                {
                    "title": title or None,
                    "link": link or None,
                    "pub_raw": pub,
                    "summary_html": body,
                    "guid": guid or link,
                }
            )
        return out

    if _local_tag(tag) == "feed":
        out = []
        for entry in root:
            if _local_tag(entry.tag) != "entry":
                continue
            title_el = link_el = id_el = updated_el = published_el = summary_el = content_el = None
            for child in entry:
                ln = _local_tag(child.tag)
                if ln == "title":
                    title_el = child
                elif ln == "link" and child.get("href"):
                    if child.get("rel") in (None, "alternate") or link_el is None:
                        link_el = child
                elif ln == "id":
                    id_el = child
                elif ln == "updated":
                    updated_el = child
                elif ln == "published":
                    published_el = child
                elif ln == "summary":
                    summary_el = child
                elif ln == "content":
                    content_el = child
            title = (title_el.text or "").strip() if title_el is not None else ""
            link = (link_el.get("href") or "").strip() if link_el is not None else ""
            pub = None
            if published_el is not None and published_el.text:
                pub = published_el.text.strip()
            elif updated_el is not None and updated_el.text:
                pub = updated_el.text.strip()
            guid = (id_el.text or "").strip() if id_el is not None else None
            body = None
            if content_el is not None:
                body = "".join(content_el.itertext()) or content_el.text
            elif summary_el is not None:
                body = summary_el.text
            out.append(
                {
                    "title": title or None,
                    "link": link or None,
                    "pub_raw": pub,
                    "summary_html": body,
                    "guid": guid or link,
                }
            )
        return out

    return []


def _build_markdown(
    *,
    ingest_date: date,
    aired_date: date | None,
    feed_url: str,
    item: dict[str, str | None],
    slug_prefix: str,
    thread: str | None = None,
) -> tuple[str, str]:
    title = item.get("title") or "untitled"
    link = item.get("link") or ""
    guid = item.get("guid") or link
    h = hashlib.sha256((guid or title).encode("utf-8")).hexdigest()[:8]
    air = aired_date or ingest_date
    slug_core = _slugify(str(title))
    filename = f"{slug_prefix}-{air.isoformat()}-{slug_core}-{h}.md"
    summary = _strip_html(str(item.get("summary_html") or ""))

    thread_line = f"thread: {thread}\n" if thread else ""
    front = (
        "---\n"
        f"ingest_date: {ingest_date.isoformat()}\n"
        f"aired_date: {air.isoformat()}\n"
        f"kind: rss-item\n"
        f"feed_url: {feed_url}\n"
        f"source_url: {link}\n"
        f"guid: {guid}\n"
        f"{thread_line}"
        "---\n\n"
    )
    body_lines = [
        f"# {title}",
        "",
        f"**Canonical link:** {link}",
        "",
    ]
    if summary:
        body_lines.append("## Summary (text extracted from feed)")
        body_lines.append("")
        body_lines.append(textwrap.fill(summary, width=92))
        body_lines.append("")
    body_lines.append("_Fetched by `scripts/fetch_strategy_raw_input.py`; not Record._")
    body_lines.append("")
    return filename, front + "\n".join(body_lines)


def load_config(path: Path) -> dict[str, Any]:
    if not path.is_file():
        raise FileNotFoundError(
            f"Missing config {path}. Copy raw-input/fetch-sources.example.json → fetch-sources.json"
        )
    return json.loads(path.read_text(encoding="utf-8"))


def run(
    *,
    config_path: Path,
    raw_root: Path,
    ingest_date: date,
    apply: bool,
    global_max: int | None,
) -> int:
    cfg = load_config(config_path)
    feeds = cfg.get("rss_feeds") or []
    planned: list[tuple[Path, str]] = []

    for feed in feeds:
        if not feed.get("enabled", True):
            continue
        url = feed.get("url")
        if not url:
            continue
        slug_prefix = feed.get("slug_prefix") or _slugify(urlparse(url).netloc or "rss")
        max_items = int(feed.get("max_items", 5))
        if global_max is not None:
            max_items = min(max_items, global_max)

        thread_str: str | None = None
        raw_tid = feed.get("thread")
        if raw_tid is not None and str(raw_tid).strip():
            tid = str(raw_tid).strip()
            if tid not in _EXPERT_IDS_SET:
                print(
                    f"WARNING: feed {url!r} has unknown thread expert_id {tid!r}; "
                    "omitting thread line in markdown",
                    flush=True,
                )
            else:
                thread_str = tid

        try:
            data = _fetch_url(str(url))
        except urllib.error.URLError as e:
            print(f"ERROR fetch {url}: {e}")
            continue

        try:
            root = ET.fromstring(data)
        except ET.ParseError as e:
            print(f"ERROR parse XML {url}: {e}")
            continue

        items = _iter_rss_items(root)[:max_items]
        for item in items:
            pub = _parse_pub_date(str(item.get("pub_raw") or "") or None)
            fname, content = _build_markdown(
                ingest_date=ingest_date,
                aired_date=pub,
                feed_url=str(url),
                item=item,
                slug_prefix=str(slug_prefix),
                thread=thread_str,
            )
            air = pub or ingest_date
            dest = raw_root / air.isoformat() / fname
            planned.append((dest, content))

    for dest, content in sorted(planned, key=lambda x: str(x[0])):
        rel = dest.relative_to(REPO_ROOT) if dest.is_relative_to(REPO_ROOT) else dest
        exists = dest.is_file()
        same = exists and dest.read_text(encoding="utf-8") == content
        if same:
            print(f"skip (unchanged): {rel}")
            continue
        if not apply:
            action = "would write" if not exists else "would update"
            print(f"{action}: {rel}")
            continue
        dest.parent.mkdir(parents=True, exist_ok=True)
        if exists:
            dest.write_text(content, encoding="utf-8")
            print(f"updated: {rel}")
        else:
            dest.write_text(content, encoding="utf-8")
            print(f"wrote: {rel}")

    if not planned:
        print("No items planned (empty feeds or fetch errors).")
    elif not apply:
        print(f"\nDry-run: {len(planned)} file(s). Pass --apply to write.")

    return 0


def _parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--config", type=Path, default=None, help="JSON config path")
    p.add_argument(
        "--root",
        type=Path,
        default=DEFAULT_RAW_ROOT,
        help="raw-input root directory",
    )
    p.add_argument("--today", type=str, default=None, help="ingest date YYYY-MM-DD (default: local today)")
    p.add_argument("--max-items", type=int, default=None, help="cap items per feed (override)")
    p.add_argument("--apply", action="store_true", help="Write files (default: dry-run)")
    p.add_argument("--dry-run", action="store_true", help="Force dry-run")
    return p.parse_args()


def main() -> int:
    import os

    args = _parse_args()
    if args.apply and args.dry_run:
        raise SystemExit("Use only one of --apply or --dry-run")
    apply = bool(args.apply)

    env_cfg = os.environ.get("FETCH_STRATEGY_SOURCES")
    config_path = args.config or (Path(env_cfg) if env_cfg else DEFAULT_CONFIG)

    ingest_date = (
        datetime.strptime(args.today, "%Y-%m-%d").date()
        if args.today
        else date.today()
    )

    return run(
        config_path=config_path,
        raw_root=args.root.resolve(),
        ingest_date=ingest_date,
        apply=apply,
        global_max=args.max_items,
    )


if __name__ == "__main__":
    raise SystemExit(main())

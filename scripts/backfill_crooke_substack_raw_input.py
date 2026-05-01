#!/usr/bin/env python3
"""Partial Crooke automation for Conflicts Forum Substack.

This helper uses the public Substack archive as a discovery layer and writes
Crooke raw-input files when the archive or post API exposes usable text. It is
designed for the paid-Substack case where the public archive can confirm the
post exists, but the full body may still require manual capture.

WORK only; not Record.

Typical use:
  python3 scripts/backfill_crooke_substack_raw_input.py --dry-run
  python3 scripts/backfill_crooke_substack_raw_input.py --apply
  python3 scripts/backfill_crooke_substack_raw_input.py --apply --check-existing
"""

from __future__ import annotations

import argparse
import sys
from datetime import date, datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_RAW_ROOT = (
    REPO_ROOT / "docs/skill-work/work-strategy/strategy-notebook/raw-input"
)
DEFAULT_HOSTNAME = "conflictsforum.substack.com"
DEFAULT_YEAR = 2026
DEFAULT_THREAD = "crooke"

_SCRIPTS = REPO_ROOT / "scripts"
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from backfill_substack_raw_input import (  # noqa: E402
    _fetch_json,
    _post_day_utc,
    _slugify,
    _strip_html,
)
from strategy_expert_transcript import iter_raw_input_yaml_documents  # noqa: E402


def _normalize_url(url: str) -> str:
    return url.strip().rstrip("/")


def _preview_marker(text: str) -> bool:
    low = text.lower()
    return any(
        marker in low
        for marker in (
            "keep reading with a 7-day free trial",
            "already a paid subscriber",
            "subscribe to continue reading",
            "sign in to continue reading",
            "keep reading",
        )
    )


def _archive_items(hostname: str, *, year: int, limit: int = 50) -> list[dict]:
    host = hostname.strip().rstrip("/")
    if host.startswith("https://"):
        host = host[len("https://") :]

    collected: list[dict] = []
    offset = 0
    while True:
        url = f"https://{host}/api/v1/archive?sort=new&offset={offset}&limit={limit}"
        try:
            batch = _fetch_json(url)
        except Exception as e:  # pragma: no cover - network and remote parsing
            print(f"warn: archive fetch failed at offset={offset}: {e}", file=sys.stderr)
            break
        if not isinstance(batch, list) or not batch:
            break

        for item in batch:
            if not isinstance(item, dict):
                continue
            try:
                d = _post_day_utc(item["post_date"])
            except Exception:
                continue
            if d.year == year:
                collected.append(item)

        if all(
            _post_day_utc(x["post_date"]) < date(year, 1, 1)
            for x in batch
            if isinstance(x, dict) and "post_date" in x
        ):
            break
        offset += len(batch)

    by_slug: dict[str, dict] = {}
    for item in collected:
        slug = str(item.get("slug") or "").strip()
        if slug:
            by_slug[slug] = item
    return sorted(by_slug.values(), key=lambda x: x.get("post_date") or "")


def _load_existing_keys(raw_root: Path, *, thread: str) -> set[str]:
    """Collect source_url, slug, and title keys already present for this thread."""
    keys: set[str] = set()
    if not raw_root.is_dir():
        return keys

    for md in raw_root.rglob("*.md"):
        if md.name == "README.md":
            continue
        try:
            text = md.read_text(encoding="utf-8")
        except OSError:
            continue
        for fm, body in iter_raw_input_yaml_documents(text):
            if (fm.get("thread") or "").strip() != thread:
                continue
            src = _normalize_url(str(fm.get("source_url") or ""))
            if src:
                keys.add(src)
            slug = str(fm.get("slug") or "").strip()
            if slug:
                keys.add(slug)
            title = ""
            for line in body.splitlines():
                if line.startswith("# "):
                    title = line[2:].strip()
                    break
            if title:
                keys.add(title.lower())
    return keys


def _build_doc(
    *,
    post: dict,
    body_text: str,
    ingest_date: date,
    thread: str,
    publication_host: str,
) -> str:
    day = _post_day_utc(post["post_date"])
    title = post.get("title") or post.get("slug") or "untitled"
    canonical = post.get("canonical_url") or f"https://{publication_host}/p/{post['slug']}"
    capture_mode = "archive-preview" if _preview_marker(body_text) or not body_text.strip() else "archive-text"
    note = (
        "Public archive discovery; paid body may need manual completion."
        if capture_mode == "archive-preview"
        else "Archive API body text captured from the public endpoint."
    )

    front = [
        "---",
        f"ingest_date: {ingest_date.isoformat()}",
        f"pub_date: {day.isoformat()}",
        "kind: substack-post",
        f"source_url: {canonical}",
        f"publication: {publication_host}",
        f"slug: {post['slug']}",
        f"post_id: {post.get('id')}",
        f"thread: {thread}",
        f"capture_mode: {capture_mode}",
        f"note: {note}",
        "---",
        "",
        f"# {title}",
        "",
        f"**Canonical:** {canonical}",
        "",
    ]

    teaser = (post.get("description") or post.get("subtitle") or "").strip()
    body = _strip_html(body_text).strip()
    if body:
        front.extend(
            [
                "## Body (archive text)",
                "",
                body,
                "",
            ]
        )
    elif teaser:
        front.extend(
            [
                "## Teaser (archive)",
                "",
                teaser,
                "",
            ]
        )

    front.extend(
        [
            "## Status",
            "",
            "_Partial Crooke automation: public archive discovery first; manual body completion remains allowed._",
            "",
        ]
    )
    return "\n".join(front)


def run(
    *,
    hostname: str,
    year: int,
    raw_root: Path,
    ingest_date: date,
    thread: str,
    apply: bool,
    limit: int,
    check_existing: bool,
) -> int:
    raw_root = raw_root.resolve()
    posts = _archive_items(hostname, year=year, limit=limit)
    existing = _load_existing_keys(raw_root, thread=thread)

    print(f"Crooke archive discovery: {len(posts)} post(s) found for {hostname} in {year}")
    if check_existing:
        print(f"Existing Crooke raw-input keys: {len(existing)}")

    wrote = 0
    matched = 0
    for post in posts:
        slug = str(post.get("slug") or "").strip()
        title = str(post.get("title") or slug or "untitled").strip()
        canonical = post.get("canonical_url") or f"https://{hostname.rstrip('/')}/p/{slug}"
        day = _post_day_utc(post["post_date"])
        dest = raw_root / day.isoformat() / f"substack-crooke-{_slugify(slug, max_len=60)}-{day.isoformat()}.md"

        key_candidates = {
            _normalize_url(str(canonical)),
            _normalize_url(str(post.get("url") or "")),
            slug,
            title.lower(),
        }
        if existing.intersection(key_candidates):
            matched += 1
            print(f"  matched: {day.isoformat()} {title}")
            continue

        try:
            detail = _fetch_json(f"https://{hostname.rstrip('/')}/api/v1/posts/{slug}")
        except Exception as e:  # pragma: no cover - network dependent
            print(f"  skip {slug}: {e}")
            continue
        if not isinstance(detail, dict):
            print(f"  skip {slug}: unexpected detail payload")
            continue

        body_text = str(detail.get("body_html") or "")
        content = _build_doc(
            post=detail,
            body_text=body_text,
            ingest_date=ingest_date,
            thread=thread,
            publication_host=hostname,
        )
        rel = dest.relative_to(REPO_ROOT)
        if dest.is_file() and dest.read_text(encoding="utf-8") == content:
            print(f"  skip unchanged: {rel}")
            matched += 1
            continue
        if not apply:
            print(f"  would write: {rel}")
            wrote += 1
            continue

        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(content, encoding="utf-8")
        wrote += 1
        print(f"  wrote: {rel}")

    print(f"Summary: matched={matched} wrote={wrote} apply={apply}")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--hostname", default=DEFAULT_HOSTNAME, help="Substack hostname")
    ap.add_argument("--year", type=int, default=DEFAULT_YEAR, help="Archive year to backfill")
    ap.add_argument("--root", type=Path, default=DEFAULT_RAW_ROOT, help="raw-input root")
    ap.add_argument("--ingest-date", type=str, default=None, help="YYYY-MM-DD ingest date")
    ap.add_argument("--thread", default=DEFAULT_THREAD, help="expert_id thread tag")
    ap.add_argument("--limit", type=int, default=50, help="Archive page size")
    ap.add_argument("--apply", action="store_true", help="Write files")
    ap.add_argument("--check-existing", action="store_true", help="Report matches against existing raw-input")
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
        check_existing=args.check_existing,
    )


if __name__ == "__main__":
    raise SystemExit(main())

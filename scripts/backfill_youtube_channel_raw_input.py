#!/usr/bin/env python3
"""Backfill a public YouTube channel into strategy-notebook raw-input/.

This is the reusable core for the graph-first YouTube queue. It can run the
existing transcript fetcher, or operate in ``--index-only`` mode to mirror
direct channel listings into strategy-notebook raw-input Markdown with routing
metadata.

WORK only; not Record.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import shutil
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import date, datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = REPO_ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from fetch_strategy_raw_input import _slugify  # noqa: E402
from youtube_transcripts.metadata import fetch_metadata_ytdlp  # noqa: E402


def _normalize_date(raw: str | None) -> str | None:
    s = (raw or "").strip()
    if not s:
        return None
    if re.fullmatch(r"\d{8}", s):
        return f"{s[:4]}-{s[4:6]}-{s[6:8]}"
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}", s):
        return s
    try:
        return datetime.fromisoformat(s.replace("Z", "+00:00")).date().isoformat()
    except ValueError:
        return None


def _split_transcript_body(text: str) -> str:
    lines = text.splitlines()
    i = 0
    while i < len(lines) and lines[i].startswith("#"):
        i += 1
    while i < len(lines) and not lines[i].strip():
        i += 1
    return "\n".join(lines[i:]).strip()


def infer_guest_from_title(title: str) -> str | None:
    """Best-effort guest inference for Dialogue Works-style titles."""
    t = " ".join(title.split())
    t = re.sub(r"\s*\(operator transcript\)\s*$", "", t, flags=re.I)
    t = re.sub(r"\s*\(clean transcript\)\s*$", "", t, flags=re.I)
    if t.lower().startswith("nima x "):
        guest = t.split("x", 1)[1].strip()
        guest = re.split(r"\s*[-–—:|]\s*", guest, maxsplit=1)[0].strip()
        return guest or None
    if t.lower().startswith("nima x "):
        guest = t.split("x", 1)[1].strip(" -_:")
        return guest or None
    m = re.match(r"^(?:Nima\s*[-–—]\s*)?(?P<guest>[^:–—-]{2,80}?)(?:\s*[:–—-]\s*.+)?$", t)
    if m:
        guest = m.group("guest").strip()
        if guest and "nima" not in guest.lower() and "dialogue works" not in guest.lower():
            return guest
    return None


def _frontmatter(
    *,
    ingest_date: str,
    pub_date: str,
    source_url: str,
    channel_url: str,
    channel_slug: str,
    title: str,
    show: str | None,
    host: str | None,
    thread: str | None,
    guest: str | None,
    source_note: str,
) -> str:
    lines = [
        "---",
        f"ingest_date: {ingest_date}",
        f"pub_date: {pub_date}",
        "kind: transcript",
    ]
    if thread:
        lines.append(f"thread: {thread}")
    if show:
        lines.append(f"show: {show}")
    if host:
        lines.append(f"host: {host}")
    if guest:
        lines.append(f"guest: {guest}")
    lines.extend(
        [
            f"title: {json.dumps(title, ensure_ascii=True)}",
            f"channel_url: {json.dumps(channel_url, ensure_ascii=True)}",
            f"channel_slug: {json.dumps(channel_slug, ensure_ascii=True)}",
            f"source_url: {json.dumps(source_url, ensure_ascii=True)}",
            f"source_note: {json.dumps(source_note, ensure_ascii=True)}",
            "---",
            "",
        ]
    )
    return "\n".join(lines)


def convert_index_to_raw_input(
    *,
    output_dir: Path,
    notebook_root: Path,
    ingest_date: str,
    apply: bool,
    channel_slug: str,
    channel_url: str,
    show: str | None,
    host: str | None,
    thread: str | None,
    file_prefix: str,
    source_note: str,
    infer_guest: bool,
    index_only: bool,
) -> int:
    index_path = output_dir / "index.json"
    if not index_path.exists():
        print(f"Missing index: {index_path}", file=sys.stderr)
        return 1
    data = json.loads(index_path.read_text(encoding="utf-8"))
    videos = data.get("videos") or []
    raw_root = notebook_root / "raw-input"
    written = 0

    for v in videos:
        status = str(v.get("status") or "").strip()
        if index_only and not status:
            status = "listed_only"
        transcript_file = str(v.get("transcript_file") or "").strip()
        allowed_statuses = {"ok", "needs_review", "skipped_existing", "skipped_unchanged"}
        if index_only:
            allowed_statuses.add("listed_only")
        if status not in allowed_statuses:
            continue
        upload_date = _normalize_date(str(v.get("upload_date") or ""))
        if not upload_date:
            print(f"skip {v.get('video_id')}: missing upload_date", file=sys.stderr)
            continue
        title = str(v.get("title") or "").strip() or str(v.get("video_id") or "untitled")
        guest = infer_guest_from_title(title) if infer_guest else None
        slug = _slugify(title, max_len=72)
        out_dir = raw_root / upload_date
        out_path = out_dir / f"{file_prefix}-{slug}-{upload_date}.md"
        if index_only:
            body = f"# {title}\n\n"
        else:
            src_path = output_dir / transcript_file
            if not src_path.exists():
                print(f"skip {v.get('video_id')}: missing transcript file {src_path}", file=sys.stderr)
                continue

            raw_text = src_path.read_text(encoding="utf-8", errors="replace")
            body = _split_transcript_body(raw_text)
            if not body:
                print(f"skip {v.get('video_id')}: empty body", file=sys.stderr)
                continue
            body = f"# {title}\n\n" + body + "\n"

        content = (
            _frontmatter(
                ingest_date=ingest_date,
                pub_date=upload_date,
                source_url=str(v.get("url") or ""),
                channel_url=channel_url,
                channel_slug=channel_slug,
                title=title,
                show=show,
                host=host,
                thread=thread,
                guest=guest,
                source_note=source_note,
            )
            + body
        )

        if out_path.exists():
            existing = out_path.read_text(encoding="utf-8", errors="replace")
            if existing == content:
                print(f"skip unchanged: {out_path.relative_to(notebook_root)}")
                continue
        if not apply:
            print(f"would write: {out_path.relative_to(notebook_root)}")
            written += 1
            continue
        out_dir.mkdir(parents=True, exist_ok=True)
        out_path.write_text(content, encoding="utf-8")
        print(f"wrote: {out_path.relative_to(notebook_root)}")
        written += 1

    if not apply and written:
        print("\nDry-run only. Pass --apply to write files.", file=sys.stderr)
    return 0


def _direct_channel_index(
    *,
    channel_url: str,
    limit: int,
) -> list[dict[str, str]]:
    """Use yt-dlp directly to list videos on a channel page."""
    python_cmd = shutil.which("python") or sys.executable
    cmd = [
        python_cmd,
        "-m",
        "yt_dlp",
        "--flat-playlist",
        "--skip-download",
        "--dump-single-json",
        "--playlist-end",
        str(max(1, limit)),
        channel_url,
    ]
    proc = subprocess.run(cmd, cwd=str(REPO_ROOT), capture_output=True, text=True)
    if proc.returncode != 0:
        raise RuntimeError(
            "yt-dlp channel listing failed:\n"
            f"{proc.stderr.strip() or proc.stdout.strip() or channel_url}"
        )
    try:
        payload = json.loads(proc.stdout)
    except json.JSONDecodeError as exc:
        raise RuntimeError(
            "yt-dlp channel listing returned non-JSON output:\n"
            f"{proc.stdout.strip()[:1000]}"
        ) from exc
    entries = payload.get("entries") or []
    rows: list[dict[str, str]] = []
    seen: set[str] = set()
    for entry in entries:
        if not entry:
            continue
        video_id = str(entry.get("id") or "").strip()
        if not video_id or video_id in seen:
            continue
        seen.add(video_id)
        title = str(entry.get("title") or "").strip()
        url = str(entry.get("url") or entry.get("webpage_url") or "").strip()
        rows.append(
            {
                "video_id": video_id,
                "title": title or video_id,
                "upload_date": "",
                "duration_seconds": "",
                "url": url or f"https://www.youtube.com/watch?v={video_id}",
                "transcript_file": None,
                "status": "listed_only",
                "language": None,
                "error": None,
            }
        )
    return rows


def backfill_channel(
    *,
    channel_url: str,
    channel_slug: str,
    show: str | None,
    host: str | None,
    thread: str | None,
    file_prefix: str,
    source_note: str,
    work_dir: Path,
    notebook_root: Path,
    ingest_date: str | None = None,
    limit: int = 20,
    sleep: float = 0.25,
    apply: bool = False,
    infer_guest: bool = False,
    index_only: bool = False,
    stop_before_date: date | None = None,
    enrich_concurrency: int = 8,
    slice_start: int | None = None,
    slice_end: int | None = None,
) -> int:
    ingest = ingest_date or date.today().isoformat()
    work_dir.mkdir(parents=True, exist_ok=True)

    if index_only:
        python_cmd = shutil.which("python") or sys.executable
        try:
            videos = _direct_channel_index(channel_url=channel_url, limit=limit)
        except RuntimeError as exc:
            print(str(exc), file=sys.stderr)
            return 1

        if not videos:
            print(f"Found 0 video(s) on {channel_url}", file=sys.stderr)
            return 1

        if slice_start is not None or slice_end is not None:
            start = max(0, int(slice_start or 0))
            end = int(slice_end) if slice_end is not None else len(videos)
            videos = videos[start:end]
            if not videos:
                print(
                    f"Found 0 video(s) in slice {start}:{end} on {channel_url}",
                    file=sys.stderr,
                )
                return 1

        # Enrich with per-video metadata so the direct channel mirror has dates
        # and stable titles even when the flat listing omits them.
        max_workers = max(1, int(enrich_concurrency or 1))
        enriched: list[dict[str, str]] = [dict(video) for video in videos]

        def _fetch(video: dict[str, str]) -> tuple[str, dict[str, object]]:
            return video["video_id"], fetch_metadata_ytdlp(video["video_id"], max_attempts=4)

        if max_workers == 1:
            futures = []
            for video in enriched:
                futures.append((_fetch(video), video["video_id"]))
        else:
            with ThreadPoolExecutor(max_workers=max_workers) as executor:
                futures = [executor.submit(_fetch, video) for video in enriched]
                for future in as_completed(futures):
                    vid, meta = future.result()
                    for video in enriched:
                        if video["video_id"] != vid:
                            continue
                        if isinstance(meta, dict) and meta:
                            upload_date = _normalize_date(str(meta.get("upload_date") or ""))
                            if upload_date:
                                video["upload_date"] = upload_date.replace("-", "")
                            title = str(meta.get("title") or "").strip()
                            if title:
                                video["title"] = title
                            dur = meta.get("duration")
                            if dur is not None:
                                video["duration_seconds"] = str(dur)
                        break
        selected_videos: list[dict[str, str]] = []
        for video in enriched:
            upload_date = _normalize_date(str(video.get("upload_date") or ""))
            if stop_before_date and upload_date:
                try:
                    if date.fromisoformat(upload_date) < stop_before_date:
                        break
                except ValueError:
                    pass
            selected_videos.append(video)
        videos = selected_videos

        payload = {
            "channel_url": channel_url,
            "input_urls": [channel_url],
            "pipeline_version": "direct-ytdlp-channel-index",
            "generated_at_utc": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
            "video_count": len(videos),
            "transcripts_attempted": 0,
            "index_mode": "direct_channel_index",
            "videos": videos,
        }
        work_dir.mkdir(parents=True, exist_ok=True)
        (work_dir / "index.json").write_text(
            json.dumps(payload, indent=2, ensure_ascii=True) + "\n",
            encoding="utf-8",
        )
        md_lines = [
            "# Channel video index",
            "",
            f"- **channel:** {channel_url}",
            f"- **video_count:** {len(videos)}",
            f"- **generated_at_utc:** {payload['generated_at_utc']}",
            "- **method:** direct yt-dlp channel crawl (index-only)",
            "- **upload_date:** per-video yt-dlp metadata; shown as YYYY-MM-DD when parseable.",
            "",
            "| # | video_id | title | upload_date | duration_s | url |",
            "|---:|---|-----|-----|---:|-----|",
        ]
        for i, v in enumerate(videos, start=1):
            title = (v["title"] or "").replace("|", "\\|")
            md_lines.append(
                f"| {i} | `{v['video_id']}` | {title} | {_normalize_date(v.get('upload_date') or '') or ''} | {v.get('duration_seconds') or ''} | {v['url']} |"
            )
        (work_dir / "CHANNEL-VIDEO-INDEX.md").write_text("\n".join(md_lines) + "\n", encoding="utf-8")
        print(
            f"Wrote {work_dir / 'index.json'} and {work_dir / 'CHANNEL-VIDEO-INDEX.md'} "
            f"({len(videos)} videos, no transcripts fetched)",
            file=sys.stderr,
        )
    else:
        fetch_script = SCRIPTS_DIR / "fetch_youtube_channel_transcripts.py"
        fetch_cmd = [
            python_cmd,
            str(fetch_script),
            "--channel",
            channel_url,
            "-o",
            str(work_dir),
            "--limit",
            str(max(1, limit)),
            "--resume",
            "--sleep",
            str(sleep),
        ]
        print("running:", " ".join(fetch_cmd), file=sys.stderr)
        proc = subprocess.run(fetch_cmd, cwd=str(REPO_ROOT))
        if proc.returncode != 0:
            return proc.returncode

    return convert_index_to_raw_input(
        output_dir=work_dir,
        notebook_root=notebook_root,
        ingest_date=ingest,
        apply=apply,
        channel_slug=channel_slug,
        channel_url=channel_url,
        show=show,
        host=host,
        thread=thread,
        file_prefix=file_prefix,
        source_note=source_note,
        infer_guest=infer_guest,
        index_only=index_only,
    )


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--channel-url", required=True)
    ap.add_argument("--channel-slug", required=True)
    ap.add_argument("--show", default="")
    ap.add_argument("--host", default="")
    ap.add_argument("--thread", default="")
    ap.add_argument("--file-prefix", default="youtube")
    ap.add_argument("--source-note", default="")
    ap.add_argument("--work-dir", type=Path, default=REPO_ROOT / ".codex-tmp" / "youtube-channel")
    ap.add_argument("--notebook-root", type=Path, default=REPO_ROOT / "docs/skill-work/work-strategy/strategy-notebook")
    ap.add_argument("--limit", type=int, default=20)
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--ingest-date", type=str, default=None, help="YYYY-MM-DD ingest_date in frontmatter")
    ap.add_argument("--sleep", type=float, default=0.25)
    ap.add_argument("--infer-guest", action="store_true")
    ap.add_argument("--index-only", action="store_true")
    ap.add_argument("--stop-before-date", type=str, default="")
    ap.add_argument("--enrich-concurrency", type=int, default=8)
    ap.add_argument("--slice-start", type=int, default=None)
    ap.add_argument("--slice-end", type=int, default=None)
    args = ap.parse_args(argv)

    return backfill_channel(
        channel_url=args.channel_url,
        channel_slug=args.channel_slug,
        show=args.show or None,
        host=args.host or None,
        thread=args.thread or None,
        file_prefix=args.file_prefix,
        source_note=args.source_note
        or f"Automated YouTube transcript fetch for {args.show or args.channel_slug}.",
        work_dir=args.work_dir,
        notebook_root=args.notebook_root,
        ingest_date=args.ingest_date,
        limit=args.limit,
        sleep=args.sleep,
        apply=args.apply,
        infer_guest=args.infer_guest,
        index_only=args.index_only,
        stop_before_date=date.fromisoformat(args.stop_before_date) if args.stop_before_date.strip() else None,
        enrich_concurrency=args.enrich_concurrency,
        slice_start=args.slice_start,
        slice_end=args.slice_end,
    )


if __name__ == "__main__":
    raise SystemExit(main())

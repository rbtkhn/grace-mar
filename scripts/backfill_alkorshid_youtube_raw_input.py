#!/usr/bin/env python3
"""Backfill Dialogue Works YouTube transcripts into strategy-notebook raw-input/.

This wrapper fetches the public Dialogue Works YouTube channel into a temporary
transcript corpus, then mirrors the transcript text into raw-input markdown with
Dialogue Works frontmatter. Host-side capture is the primary goal; guest lanes
can still be mirrored separately when needed.
WORK only; not Record.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from datetime import date, datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = REPO_ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from fetch_strategy_raw_input import _slugify  # noqa: E402

DEFAULT_CHANNEL_URL = "https://www.youtube.com/@dialogueworks01/videos"
DEFAULT_THREAD = "alkorshid"
DEFAULT_SHOW = "Dialogue Works"
DEFAULT_HOST = "Nima Alkhorshid"


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


def _infer_guest(title: str) -> str:
    t = " ".join(title.split())
    t = re.sub(r"\s*\(operator transcript\)\s*$", "", t, flags=re.I)
    t = re.sub(r"\s*\(clean transcript\)\s*$", "", t, flags=re.I)
    if t.lower().startswith("nima x "):
        return t.split("x", 1)[1].strip(" -—:")
    m = re.match(r"^(?:Nima\s*[—–-]\s*)?(?P<guest>[^:–—-]{2,80}?)(?:\s*[:–—-]\s*.+)?$", t)
    if m:
        guest = m.group("guest").strip()
        if guest and "nima" not in guest.lower() and "dialogue works" not in guest.lower():
            return guest
    return "unknown"


def _frontmatter(*, ingest_date: str, pub_date: str, source_url: str, title: str, guest: str) -> str:
    lines = [
        "---",
        f"ingest_date: {ingest_date}",
        f"pub_date: {pub_date}",
        "kind: transcript",
        f"thread: {DEFAULT_THREAD}",
        f"show: {DEFAULT_SHOW}",
        f"host: {DEFAULT_HOST}",
        f"guest: {guest}",
        f"title: {json.dumps(title, ensure_ascii=True)}".replace('"', "", 1).replace('"', "", 1),
        f"source_url: {source_url}",
        "source_note: Automated YouTube transcript fetch for Dialogue Works host capture.",
        "---",
        "",
    ]
    return "\n".join(lines)


def _convert_index_to_raw_input(*, output_dir: Path, notebook_root: Path, ingest_date: str, apply: bool) -> int:
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
        transcript_file = str(v.get("transcript_file") or "").strip()
        if not transcript_file or status not in {"ok", "needs_review", "skipped_existing", "skipped_unchanged"}:
            continue
        upload_date = _normalize_date(str(v.get("upload_date") or ""))
        if not upload_date:
            print(f"skip {v.get('video_id')}: missing upload_date", file=sys.stderr)
            continue
        src_path = output_dir / transcript_file
        if not src_path.exists():
            print(f"skip {v.get('video_id')}: missing transcript file {src_path}", file=sys.stderr)
            continue

        raw_text = src_path.read_text(encoding="utf-8", errors="replace")
        body = _split_transcript_body(raw_text)
        if not body:
            print(f"skip {v.get('video_id')}: empty body", file=sys.stderr)
            continue

        title = str(v.get("title") or "").strip() or str(v.get("video_id") or "untitled")
        guest = _infer_guest(title)
        slug = _slugify(title, max_len=72)
        out_dir = raw_root / upload_date
        out_path = out_dir / f"transcript-dialogue-works-{slug}-{upload_date}.md"
        content = (
            _frontmatter(
                ingest_date=ingest_date,
                pub_date=upload_date,
                source_url=str(v.get("url") or ""),
                title=title,
                guest=guest,
            )
            + f"# {title}\n\n"
            + body
            + "\n"
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


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--channel-url", default=DEFAULT_CHANNEL_URL)
    ap.add_argument("--work-dir", type=Path, default=REPO_ROOT / ".codex-tmp" / "alkorshid-dialogue-works")
    ap.add_argument("--notebook-root", type=Path, default=REPO_ROOT / "docs/skill-work/work-strategy/strategy-notebook")
    ap.add_argument("--limit", type=int, default=20)
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--ingest-date", type=str, default=None, help="YYYY-MM-DD ingest_date in frontmatter")
    ap.add_argument("--sleep", type=float, default=0.25)
    args = ap.parse_args()

    ingest_date = args.ingest_date or date.today().isoformat()
    args.work_dir.mkdir(parents=True, exist_ok=True)

    fetch_script = SCRIPTS_DIR / "fetch_youtube_channel_transcripts.py"
    fetch_cmd = [
        sys.executable,
        str(fetch_script),
        "--channel",
        args.channel_url,
        "-o",
        str(args.work_dir),
        "--limit",
        str(max(1, args.limit)),
        "--resume",
        "--sleep",
        str(args.sleep),
    ]
    print("running:", " ".join(fetch_cmd), file=sys.stderr)
    proc = subprocess.run(fetch_cmd, cwd=str(REPO_ROOT))
    if proc.returncode != 0:
        return proc.returncode

    return _convert_index_to_raw_input(
        output_dir=args.work_dir,
        notebook_root=args.notebook_root,
        ingest_date=ingest_date,
        apply=args.apply,
    )


if __name__ == "__main__":
    raise SystemExit(main())

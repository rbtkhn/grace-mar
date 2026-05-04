#!/usr/bin/env python3
"""Build the Dialogue Works metadata-only episode index from the YouTube crawl.

This script intentionally stops at metadata:
- it uses the public Dialogue Works YouTube crawl
- it filters to 2026-01-01 onward
- it renders titles, dates, URLs, guest inference, and routing notes
- it marks whether a matching raw-input row already exists

No transcript body backfill happens here.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = REPO_ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from fetch_strategy_raw_input import _slugify  # noqa: E402

CHANNEL_URL = "https://www.youtube.com/@dialogueworks01/videos"
START_DATE = date(2026, 1, 1)
PROFILE_PATH = REPO_ROOT / "docs/skill-work/work-strategy/strategy-notebook/experts/alkorshid/profile.md"
INVENTORY_PATH = REPO_ROOT / "docs/skill-work/work-strategy/strategy-notebook/raw-input/dialogue-works-inventory.md"

ROUTE_HINTS = (
    ("larry c. johnson", "thread: johnson"),
    ("col. larry wilkerson", "thread: johnson"),
    ("larry wilkerson", "thread: johnson"),
    ("amb. chas freeman", "thread: freeman"),
    ("chas freeman", "thread: freeman"),
    ("alastair crooke", "thread: crooke"),
    ("scott ritter", "thread: ritter"),
)


@dataclass(frozen=True)
class DialogueWorksRow:
    pub_date: str
    title: str
    url: str
    guest: str
    routing_note: str
    raw_input_note: str


def normalize_title(title: str) -> str:
    return " ".join((title or "").split()).strip()


def infer_guest_from_title(title: str) -> str:
    """Best-effort guest inference for Dialogue Works titles."""
    t = normalize_title(title)
    t = re.sub(r"\s*\((?:operator transcript|clean transcript)\)\s*$", "", t, flags=re.I)
    if t.lower().startswith("nima x "):
        guest = t[7:].strip()
        guest = re.split(r"\s*[-â€“â€”:|]\s*", guest, maxsplit=1)[0].strip()
        return guest
    guest = re.split(r"\s*[:â€“â€”-]\s*", t, maxsplit=1)[0].strip()
    lowered = guest.lower()
    if lowered in {"nima", "nima alkhorshid", "dialogue works", "dialogue works (nima)"}:
        return ""
    return guest


def infer_routing_note(guest: str, title: str) -> str:
    haystack = f"{guest} {title}".lower()
    for needle, route in ROUTE_HINTS:
        if needle in haystack:
            return route
    return "host-hub"


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


def load_crawl_rows(index_path: Path, *, start_date: date) -> list[dict[str, str]]:
    payload = json.loads(index_path.read_text(encoding="utf-8"))
    rows: list[dict[str, str]] = []
    cutoff = start_date.isoformat()
    # yt-dlp channel listings are newest-first, so once we pass the cutoff date we can stop.
    for v in payload.get("videos") or []:
        upload_date = _normalize_date(str(v.get("upload_date") or ""))
        if not upload_date:
            continue
        if upload_date < cutoff:
            break
        rows.append(
            {
                "video_id": str(v.get("video_id") or "").strip(),
                "title": normalize_title(str(v.get("title") or "")),
                "upload_date": upload_date,
                "url": str(v.get("url") or "").strip(),
            }
        )
    rows.sort(key=lambda row: (row["upload_date"], row["title"]))
    return rows


def _raw_input_match_status(raw_input_root: Path, row: dict[str, str]) -> str:
    video_id = row["video_id"]
    title = row["title"]
    url = row["url"]
    title_slug = _slugify(title, max_len=96).lower()

    for path in raw_input_root.rglob("*.md"):
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        head = "\n".join(text.splitlines()[:25]).lower()
        if url and url.lower() in head:
            return "mirrored"
        if video_id and video_id.lower() in head:
            return "mirrored"
        if title and title.lower() in head:
            return "mirrored"
        if title_slug and title_slug == path.stem.lower():
            return "mirrored"
    return "needs capture"


def build_rows(*, crawl_index: Path, raw_input_root: Path) -> list[DialogueWorksRow]:
    base_rows = load_crawl_rows(crawl_index, start_date=START_DATE)
    out: list[DialogueWorksRow] = []
    for row in base_rows:
        guest = infer_guest_from_title(row["title"])
        routing_note = infer_routing_note(guest, row["title"])
        raw_status = _raw_input_match_status(raw_input_root, row)
        out.append(
            DialogueWorksRow(
                pub_date=row["upload_date"],
                title=row["title"],
                url=row["url"],
                guest=guest or "host-hub",
                routing_note=routing_note,
                raw_input_note=raw_status,
            )
        )
    return out


def render_table(rows: list[DialogueWorksRow]) -> str:
    lines = [
        "| pub_date | Title | Guest | URL | Routing / note | raw-input |",
        "|----------|-------|-------|-----|----------------|-----------|",
    ]
    for row in rows:
        title = row.title.replace("|", "\\|")
        guest = row.guest.replace("|", "\\|")
        route = row.routing_note.replace("|", "\\|")
        raw_note = row.raw_input_note.replace("|", "\\|")
        lines.append(
            f"| {row.pub_date} | {title} | {guest} | [{row.url}]({row.url}) | {route} | {raw_note} |"
        )
    return "\n".join(lines)


def render_profile(rows: list[DialogueWorksRow]) -> str:
    table = render_table(rows)
    return f"""# Strategy expert - `alkorshid`
<!-- word_count: ~700 -->

WORK only; not Record.

**Canonical index:** [strategy-commentator-threads.md](strategy-commentator-threads.md) - **`alkorshid`** lane.

---

## Identity

| Field | Value |
|-------|-------|
| **Name** | Nima Alkorshid |
| **expert_id** | `alkorshid` |
| **Role** | Dialogue Works host / interviewer for long-form geopolitical dialogue; use `thread:alkorshid` alongside `thread:<guest>` on shared episodes so inbox triage and raw-input thread lists mirror both sides. |
| **Default grep tags** | `Alkorshid`, `Dialogue Works`, or `DialogueWorks` in cold |
| **Typical pairings** | x `marandi`, x `diesen`, x `mercouris`, x `davis` |
| **Notebook-use tags** | `narrate` |

<a id="voice-fingerprint-compact"></a>

## Voice fingerprint (compact) - Tier B

| Field | Value |
|-------|-------|
| **Voice tier** | `B` |
| **Voice fingerprint - last reviewed** | `2026-04` |

Promotion and refresh defaults: [strategy-expert-template.md section Voice fingerprint (compact)](strategy-expert-template.md#voice-fingerprint-compact).

## Convergence fingerprint

*Minimal lane - operator extends when upgraded.*

## Tension fingerprint

*Minimal lane - operator extends when upgraded.*

## Signature mechanisms

- Interview framing: sets agenda and follow-ups; distinguish host routing from guest analytic claims on the same ingest.

## Failure modes / overreads

- Guest `thread:` lines without `thread:alkorshid` on the same episode can create asymmetric raw-input mirroring; fix by adding the host line when host prompts are load-bearing.

## Archive / backfill note

- Archive discovery is useful, but it is not a completeness mandate.
- Treat Dialogue Works as a discovery index; capture only substantial episodes worth preserving.
- Automation feeds `raw-input/` only. Pages and thread files are composed later in a separate pass.
- Host prompts matter on shared episodes, so keep `thread:alkorshid` when the host framing is load-bearing.

## Automation target

1. `https://www.youtube.com/@dialogueworks01/videos` -> `thread: alkorshid`
2. Graph-first YouTube queue: [`youtube-transcript-queue.md`](../../raw-input/youtube-transcript-queue.md) and [`scripts/backfill_youtube_channel_raw_input.py`](../../../../../scripts/backfill_youtube_channel_raw_input.py)

## Published sources (operator web index)

Where Dialogue Works / host content is published (no Wikipedia). Re-verify URLs before cite-grade use.

1. https://www.youtube.com/@dialogueworks01 - Dialogue Works (YouTube)
2. https://www.podchaser.com/podcasts/dialogue-works-5841625 - podcast index (metadata)
3. https://shows.acast.com/dialogueworks - Acast show page (when cite-grade episode URLs are needed)

## Dialogue Works episode inventory

Metadata-only index from the public YouTube crawl starting at `2026-01-01` through the latest upload returned by the crawl. Transcript bodies are not backfilled in this pass. `needs capture` means the episode is visible on the channel but not yet mirrored in `raw-input/`.

{table}

---

**Companion files:** [`transcript.md`](transcript.md) (7-day rolling verbatim) and [`thread.md`](thread.md) (distilled analytical thread).
"""


def render_inventory(rows: list[DialogueWorksRow]) -> str:
    table = render_table(rows)
    return f"""# Dialogue Works â€” metadata index
<!-- word_count: ~500 -->

**Purpose:** Metadata-only index of **Dialogue Works** (host **Nima Alkhorshid**) from the public YouTube crawl starting at **`2026-01-01`** through the latest upload returned by the crawl. Transcript bodies are not backfilled in this pass. **WORK only** â€” not Record.

**Last audited:** 2026-05-01 â€” YouTube index-only crawl with metadata enrichment.

**Routing reminder:** For symmetric expert mirroring, same-episode ingests should carry **`thread:<guest>`** plus **`thread:alkorshid`** where host prompts matter â€” see [`experts/alkorshid/profile.md`](../experts/alkorshid/profile.md).

{table}
"""


def update_block(path: Path, anchor: str, replacement: str) -> None:
    text = path.read_text(encoding="utf-8")
    idx = text.find(anchor)
    if idx < 0:
        raise RuntimeError(f"Could not find anchor {anchor!r} in {path}")
    prefix = text[:idx].rstrip()
    path.write_text(prefix + "\n\n" + replacement.strip() + "\n", encoding="utf-8")


def run_crawl(*, crawl_output_dir: Path, limit: int, sleep: float) -> Path:
    crawl_output_dir.mkdir(parents=True, exist_ok=True)
    fetch_script = SCRIPTS_DIR / "fetch_youtube_channel_transcripts.py"
    cmd = [
        sys.executable,
        str(fetch_script),
        "--index-only",
        "--enrich-metadata",
        "--channel",
        CHANNEL_URL,
        "--stop-before-date",
        START_DATE.isoformat(),
        "-o",
        str(crawl_output_dir),
        "--limit",
        str(limit),
        "--sleep",
        str(sleep),
    ]
    print("running:", " ".join(cmd), file=sys.stderr)
    proc = subprocess.run(cmd, cwd=str(REPO_ROOT))
    if proc.returncode != 0:
        raise SystemExit(proc.returncode)
    return crawl_output_dir / "index.json"


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--crawl-output-dir", type=Path, default=REPO_ROOT / ".codex-tmp" / "dialogue-works-metadata-index")
    ap.add_argument("--index-json", type=Path, default=None, help="Optional prebuilt index.json to consume instead of crawling")
    ap.add_argument("--limit", type=int, default=0, help="Max videos to crawl (0 = all)")
    ap.add_argument("--sleep", type=float, default=0.1)
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args(argv)

    crawl_index = args.index_json
    if crawl_index is None:
        crawl_index = run_crawl(crawl_output_dir=args.crawl_output_dir, limit=args.limit, sleep=args.sleep)

    rows = build_rows(crawl_index=crawl_index, raw_input_root=REPO_ROOT / "docs/skill-work/work-strategy/strategy-notebook/raw-input")
    profile_text = render_profile(rows)
    inventory_text = render_inventory(rows)

    if not args.apply:
        print(profile_text)
        print("\n" + "=" * 80 + "\n")
        print(inventory_text)
        return 0

    PROFILE_PATH.write_text(profile_text, encoding="utf-8")
    INVENTORY_PATH.write_text(inventory_text, encoding="utf-8")
    print(f"wrote: {PROFILE_PATH}")
    print(f"wrote: {INVENTORY_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

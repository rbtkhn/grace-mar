#!/usr/bin/env python3
"""
Extract speaker-tagged blocks from a cleaned strategy raw-input transcript (markdown).

Use when building **lane-split** refined pages: `### Verbatim` for each expert must be
**that speaker’s lines from the shared raw file** (same words as raw), not paraphrase.
See docs/skill-work/work-strategy/strategy-notebook/refined-page-template.md (SSOT stack).

Example (Diesen × Crooke):
  python3 scripts/strategy/extract_transcript_speaker_lanes.py \\
    docs/skill-work/work-strategy/strategy-notebook/raw-input/2026-04-27/transcript-diesen-crooke-iran-global-war-world-order-2026-04-27.md
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path

SPEAKER_RE = re.compile(
    r"(\*\*(?:Glenn Diesen|Alastair Crooke|Scott Ritter|John Mearsheimer):\*\*)"
)


def _body_after_frontmatter(text: str) -> str:
    if text.startswith("---"):
        try:
            end = text.index("---", 3) + 3
            return text[end:].lstrip()
        except ValueError:
            pass
    return text


def _strip_to_title(body: str) -> str:
    if "# " in body:
        i = body.index("# ")
        return body[i:]
    return body


def extract_lanes(
    text: str,
    patterns: list[str] | None = None,
) -> dict[str, str]:
    """
    Split on **Name:** labels. Default patterns: Glenn Diesen, Alastair Crooke.
    Returns map lowercased first name -> joined chunks (or use custom keys via patterns order).
    """
    body = _strip_to_title(_body_after_frontmatter(text))
    if patterns is None:
        pat = SPEAKER_RE
    else:
        esc = [re.escape(p) for p in patterns]
        pat = re.compile("(" + "|".join(esc) + ")")

    idx = [m for m in pat.finditer(body)]
    out: dict[str, str] = {}
    for i, m in enumerate(idx):
        label = m.group(1)
        # key: first word of name inside **Name:**
        inner = label.strip("*").split(":")[0].strip()
        key = inner.lower().split()[0] if inner else f"chunk{i}"
        start = m.start()
        endp = idx[i + 1].start() if i + 1 < len(idx) else len(body)
        chunk = body[start:endp].strip()
        if key in out:
            out[key] = out[key] + "\n\n" + chunk
        else:
            out[key] = chunk
    return out


def main() -> None:
    ap = argparse.ArgumentParser(description="Extract speaker blocks from raw-input transcript.")
    ap.add_argument("transcript", type=Path, help="Path to raw-input .md transcript")
    ap.add_argument(
        "--print",
        action="append",
        dest="print_keys",
        metavar="KEY",
        help="Print lane for key (glenn, alastair, scott, john). Repeat for multiple.",
    )
    ap.add_argument("--list", action="store_true", help="List detected keys and exit")
    args = ap.parse_args()
    text = args.transcript.read_text(encoding="utf-8")
    lanes = extract_lanes(text)
    if args.list:
        for k, v in sorted(lanes.items()):
            print(f"{k}\t{len(v)} chars")
        return
    if args.print_keys:
        for k in args.print_keys:
            # allow glenn -> glenn, alastair -> alastair
            hit = next((x for x in lanes if x == k or x.startswith(k[:4])), None)
            if not hit and k in ("diesen",):
                hit = "glenn"
            if not hit and k in ("crooke", "mearsheimer", "ritter"):
                for cand in ("alastair", "john", "scott"):
                    if cand in lanes:
                        if (k == "crooke" and cand == "alastair") or (
                            k == "mearsheimer" and cand == "john"
                        ) or (k == "ritter" and cand == "scott"):
                            hit = cand
                            break
            if hit and hit in lanes:
                print(lanes[hit])
            else:
                print(f"<!-- no lane for {k!r} keys={list(lanes)} -->", file=__import__("sys").stderr)
                raise SystemExit(1)
        return
    for k in sorted(lanes):
        print(f"### {k}\n\n{lanes[k]}\n")


if __name__ == "__main__":
    main()

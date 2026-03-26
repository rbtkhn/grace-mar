#!/usr/bin/env python3
"""
Rebuild Endgame rsi7cDRUrmE lecture transcript with conservative speaker labels.

Opening: trailer + book promo + first Q/A splits are regex-verified.
Main body: caption paragraphs preserved without per-line diarization (captions
often merge speakers; automated ?-heuristics mis-label long Jiang answers).
"""
from __future__ import annotations

import re
import sys
from pathlib import Path


def load_transcript_body(lecture_path: Path) -> str:
    text = lecture_path.read_text(encoding="utf-8")
    _, _, rest = text.partition("## Full transcript\n\n")
    if not rest.strip():
        raise SystemExit("No ## Full transcript in " + str(lecture_path))
    return rest.strip()


def split_opening(body: str) -> tuple[str, str, str, str, str]:
    """Return teaser, host_book, jiang_thanks, host_q1, remainder."""
    body = re.sub(r"\s+", " ", body).strip()
    m = re.search(
        r"(Hi friends, it's a pleasure to tell you that)",
        body,
        re.I,
    )
    if not m:
        raise SystemExit("Could not find book promo start")
    teaser = body[: m.start()].strip()
    rest = body[m.start() :]
    m2 = re.search(
        r"(Thanks so much for inviting me\.)\s*(Yeah, I want to start out with how you grew up\.)",
        rest,
        re.I | re.S,
    )
    if not m2:
        raise SystemExit("Could not split thanks / first host question")
    host_book = rest[: m2.start(1)].strip()
    jiang_thanks = m2.group(1).strip()
    host_q1 = m2.group(2).strip()
    remainder = rest[m2.end() :].strip()
    return teaser, host_book, jiang_thanks, host_q1, remainder


def wrap_fill(text: str, width: int = 92) -> str:
    import textwrap

    return textwrap.fill(text, width=width, break_long_words=False, break_on_hyphens=False)


def rebuild_lecture(lecture_path: Path) -> None:
    raw_full = lecture_path.read_text(encoding="utf-8")
    _, _, full_tail = raw_full.partition("## Full transcript\n\n")
    orig_paras = [p.strip() for p in full_tail.split("\n\n") if p.strip()]
    body = "\n\n".join(orig_paras)
    teaser, host_book, jiang_thanks, host_q1, _remainder = split_opening(
        re.sub(r"\s+", " ", body).strip()
    )

    try:
        tail_idx = next(
            i
            for i, p in enumerate(orig_paras)
            if p.strip().lower().startswith("uh you grew up in canada")
        )
    except StopIteration as exc:
        raise SystemExit("Could not find 'Uh you grew up' paragraph") from exc
    tail_paras = orig_paras[tail_idx:]

    def split_first_mixed(p: str) -> tuple[str, str] | tuple[None, None]:
        """Split host Q ending in ? from Jiang answer starting So um I grew up."""
        flat = " ".join(p.split())
        m = re.search(r"^(.*?right\?)\s+(So um I grew up\b.*)$", flat, re.I | re.S)
        if not m:
            return None, None
        return m.group(1).strip(), m.group(2).strip()

    parts = [
        "### Trailer and consciousness (clip)",
        "",
        "**Jiang Xueqin:** " + wrap_fill(teaser),
        "",
        "### Channel promo and introduction",
        "",
        "**Host (Endgame):** " + wrap_fill(host_book),
        "",
        "**Jiang Xueqin:** " + wrap_fill(jiang_thanks),
        "",
        "**Host (Endgame):** " + wrap_fill(host_q1),
        "",
        "### Conversation (captions)",
        "",
        "_YouTube captions do not separate speakers; paragraphs below follow the published English subtitles (same text as before). Use for search and book lane; optional manual pass for Host/Jiang if needed._",
        "",
    ]
    first = tail_paras[0]
    a, b = split_first_mixed(first)
    if a and b:
        parts.append("**Host (Endgame):** " + wrap_fill(a))
        parts.append("")
        parts.append("**Jiang Xueqin:** " + wrap_fill(b))
        parts.append("")
        rest_tail = tail_paras[1:]
    else:
        rest_tail = tail_paras
    for p in rest_tail:
        parts.append(wrap_fill(" ".join(p.split())))
        parts.append("")

    new_body = "\n".join(parts).rstrip() + "\n"

    head, _, _ = raw_full.partition("## Full transcript")
    meta = head.replace(
        "**Transcript:** YouTube English captions, normalized (timestamps and markup stripped; continuous read without speaker diarization).",
        "**Transcript:** YouTube English captions, normalized (timestamps and markup stripped). **Opening** segments are speaker-labeled; **main body** follows caption paragraphs (speakers often merged in source).",
    )
    if "Opening segments" not in meta:
        # header line might differ
        meta = re.sub(
            r"\*\*Transcript:\*\*[^\n]+",
            "**Transcript:** YouTube English captions, normalized (timestamps and markup stripped). **Opening** segments are speaker-labeled; **main body** follows caption paragraphs (speakers often merged in source).",
            meta,
            count=1,
        )

    lecture_path.write_text(meta + "## Full transcript\n\n" + new_body, encoding="utf-8")


def main() -> None:
    out = Path("research/external/work-jiang/lectures/interviews-10-endgame-our-true-wealth-is-our-consciousness.md")
    if len(sys.argv) > 1:
        out = Path(sys.argv[1])
    rebuild_lecture(out)
    print("Wrote", out)


if __name__ == "__main__":
    main()

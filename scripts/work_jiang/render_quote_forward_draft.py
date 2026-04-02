#!/usr/bin/env python3
"""Emit quote-forward chapter draft.md from curated lecture (Full transcript section).

Pilot for Volume I: mostly verbatim blockquotes + short gloss paragraphs.
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
WORK = REPO / "research/external/work-jiang"

CHAPTERS = {
    "ch01": {
        "lecture": WORK / "lectures/geo-strategy-01-iran-strategy-matrix-2024-04-24.md",
        "title": "Geo-Strategy #1: Iran's Strategy Matrix",
        "video_id": "xEEpOxqdU5E",
        "thesis": (
            "This chapter lets Jiang’s **Geo-Strategy #1** run long on the page: "
            "military dominance versus **asymmetrical warfare**, the **Iran strategy matrix**, "
            "and **Operation True Promise** read as a strategy case. Glosses only orient; "
            "wording inside blockquotes is from the **curated lecture transcript** (ASR lineage)."
        ),
        "glosses": [
            "Opens on the **Damascus embassy** strike, **military dominance** (tech + intelligence), and the "
            "**True Promise** framing dispute (interception bragging vs. **designed restraint**).",
            "**Asymmetrical warfare** (carriers vs. drones, **True Promise** cost sketch), **Millennium Challenge** "
            "“cheating,” **empire inflexibility**, **Vietnam**; then the **four** simultaneous pre-invasion moves.",
            "**Iran strategy matrix** named and unpacked: **1953**, **axis of resistance**, **Russia/China** conditions, "
            "**Gaza** / opinion, **coalition friction**—through the **weaken-the-enemy** logic.",
            "**Operation True Promise** walked row-by-row; **disproportionality** and U.S. restraint; then **rules of "
            "engagement** and class **tail** (Israel hubris, **empire** stress—preview of later lectures). "
            "Verify cost figures before print.",
        ],
    },
    "ch02": {
        "lecture": WORK / "lectures/geo-strategy-02-christian-zionism-middle-east-conflict.md",
        "title": "Geo-Strategy #2: Christian Zionism and the Middle East Conflict",
        "video_id": "lkKrZq4YdqY",
        "thesis": (
            "This chapter is **quote-forward** on **Geo-Strategy #2**: why the U.S. might invade Iran "
            "through **empire**, **allies**, and the **Israel Lobby**, developed as a **compressed "
            "history of Christianity**, **end-times splits**, **Christian Zionism**, and U.S. **Bible-first** "
            "lineage. Glosses mark pedagogy versus historiography; blockquotes follow the **curated transcript**."
        ),
        "glosses": [
            "Forecast: an **eventual** U.S. invasion of Iran (timing open). **Three reasons**: defend "
            "**empire**, **ally pressure** (Saudi Arabia, Israel), then **Israel Lobby**—but theology first.",
            "**Second Coming** narrative; early Christianity as a **revolutionary** appeal to the oppressed—"
            "Jiang calls it a **free lottery ticket**; **Augustine** recenters **establishment** Christianity "
            "and blunts imminent **Second Coming** anxiety (**amillennial**-style move in lecture terms).",
            "**Reformation** → **Bible supreme**; **England**, **dissenters**, transport to **America**; "
            "inner U.S. story as **Christian nation**—use as **lecture map**, not balanced constitutional history.",
            "**Four end-times** families (**historic** vs **dispensational** “promise” vs “plan”); **organized** "
            "minority + **inequality** soil; **Middle East** as prophetic theater; **Christian Zionism**, **Zionism**, "
            "**1948**; closing **summary** + **Q&A** (**Pax Americana** / class rhetoric as **pedagogical provocation**, "
            "distinct from the theology chain).",
        ],
    },
}


def flowing_transcript(md_path: Path) -> str:
    lines = md_path.read_text(encoding="utf-8").splitlines()
    idx = next(i for i, ln in enumerate(lines) if ln.strip() == "## Full transcript")
    body: list[str] = []
    for ln in lines[idx + 1 :]:
        if ln.startswith("## ") and body:
            break
        body.append(ln)
    return " ".join(ln.strip() for ln in body if ln.strip())


def chunk_on_okay_cadence(text: str, target_words: int = 950) -> list[str]:
    """Split on frequent classroom ' okay ' breaks so blocks don't start mid-sentence."""
    segments = [s.strip() for s in text.split(" okay ") if s.strip()]
    chunks: list[str] = []
    buf: list[str] = []
    for seg in segments:
        buf.append(seg)
        block = " okay ".join(buf) + " okay"
        if len(block.split()) >= target_words:
            chunks.append(block)
            buf = []
    if buf:
        chunks.append(" okay ".join(buf))
    if len(chunks) >= 2 and len(chunks[-1].split()) < 80:
        chunks[-2] = chunks[-2] + " " + chunks[-1]
        chunks.pop()
    # Re-attach thin orphan starters (split after " okay " mid-clause); avoid merging broad "so".
    merged: list[str] = []
    orphan = re.compile(
        r"^(um|but)\b|^(and this is)\b|^(um but)\b",
        re.I,
    )
    for c in chunks:
        c = c.strip()
        force_merge = bool(re.match(r"^um but\b", c, re.I))
        if merged and (force_merge or (orphan.match(c) and len(c.split()) < 400)):
            merged[-1] = merged[-1] + " " + c
        else:
            merged.append(c)
    return merged


def render(chapter_id: str) -> str:
    cfg = CHAPTERS[chapter_id]
    raw = flowing_transcript(cfg["lecture"])
    parts = chunk_on_okay_cadence(raw, target_words=950)
    slots = max(0, len(parts) - 1)
    glosses = list(cfg["glosses"][:slots])
    if len(glosses) < slots:
        glosses.extend(
            ["*(Continue in curated lecture file.)*" for _ in range(slots - len(glosses))]
        )
    lines_out: list[str] = [
        f"# {chapter_id} — {cfg['title']}",
        "",
        "**Format (pilot):** Quote-forward Volume I draft — blockquotes are **verbatim lecture transcript** "
        f"from [`{cfg['lecture'].relative_to(WORK)}`](../../{cfg['lecture'].relative_to(WORK)}). "
        f"Recording: `https://www.youtube.com/watch?v={cfg['video_id']}`. See "
        "[`book/VOLUME-I-QUOTE-FORWARD-PILOT.md`](../../book/VOLUME-I-QUOTE-FORWARD-PILOT.md).",
        "",
        "## Thesis (book voice)",
        "",
        cfg["thesis"],
        "",
        "## Lecture excerpts",
        "",
    ]
    for i, block in enumerate(parts):
        lines_out.append(f"### Part {i + 1}")
        lines_out.append("")
        lines_out.append("> " + block)
        lines_out.append("")
        if i < len(parts) - 1:
            lines_out.append(f"**Gloss:** {glosses[i]}")
            lines_out.append("")
    note_extra = ""
    if chapter_id == "ch01":
        note_extra = (
            "**Tail of lecture:** after the matrix / True Promise case, the class continues into "
            "**rules of engagement**, **strategic ambiguity**, and student caveats — see the full "
            "curated lecture file for the remainder.\n\n"
        )
    lines_out.extend(
        [
            "## Note",
            "",
            note_extra
            + "Word-count split is **mechanical** (≈950 words per block) for readability on screen; "
            "editorial pass may restore **paragraph breaks** or **timestamps** before publication.",
            "",
        ]
    )
    return "\n".join(lines_out)


def main() -> None:
    p = argparse.ArgumentParser(description="Render quote-forward draft.md for ch01/ch02.")
    p.add_argument(
        "chapters",
        nargs="+",
        choices=["ch01", "ch02"],
        help="Chapter ids to render",
    )
    p.add_argument(
        "--dry-run",
        action="store_true",
        help="Print chunk stats only",
    )
    args = p.parse_args()
    for cid in args.chapters:
        cfg = CHAPTERS[cid]
        raw = flowing_transcript(cfg["lecture"])
        parts = chunk_on_okay_cadence(raw, target_words=950)
        print(f"{cid}: {len(raw.split())} words -> {len(parts)} blocks")
        if args.dry_run:
            continue
        out = WORK / "chapters" / cid / "draft.md"
        out.write_text(render(cid), encoding="utf-8")
        print(f"Wrote {out}")


if __name__ == "__main__":
    main()

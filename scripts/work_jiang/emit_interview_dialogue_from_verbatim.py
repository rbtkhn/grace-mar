#!/usr/bin/env python3
"""Build speaker-labeled markdown for an interview from verbatim-transcripts/*.md.

Heuristic labels (keyword + tie-break alternation). Operator must verify against audio
before book quotations. See ASR-VERIFICATION-RUBRIC.md.

Usage:
  python3 scripts/work_jiang/emit_interview_dialogue_from_verbatim.py \\
    --verbatim research/external/work-jiang/verbatim-transcripts/interviews-12-j-shapiro-truth-myth-personal-path.md \\
    --output /tmp/out.md
"""
from __future__ import annotations

import argparse
import re
import unicodedata
from pathlib import Path

JAY = (
    "lummit podcast",
    "professor xiang",
    "professor jiang",
    "my guest today",
    "i'll be back at the end",
    "like and subscribe",
    "dead sea scrolls",
    "masada will never fall",
    "i grew up",
    "hebrew school",
    "i'm not a historian",
    "from my perspective",
    "from again my per",
    "i i think that's still",
    "i run into this",
    "my sort of experience",
    "i was near new york",
    "william guy carr",
    "i i can't speak on",
    "i consider myself pretty strongly atheistic",
    "i don't get a lot out of it",
    "how does all of this kind of knowledge",
    "i guess i'm still a little stuck",
    "just need to know that",
    "i won't keep you long on the intro",
    "hijacking history right",
    "so yeah so we were in israel for a week",
    "i did go to israel",
    "sheldon alderson",
    "i opted out of it",
    "filmmaker",
    "i'm a documentary filmmaker",
    "eric from",
    "escape from freedom",
    "jeffrey epstein had the talmud",
    "if i could just put out sort of my hypothesis",
    "i put the blame on the myth makers",
)

JIANG = (
    "i was born in 1976",
    "my background is",
    "my family um was very poor",
    "we went to canada",
    "i came in 99",
    "i have a ba in english",
    "great books",
    "i'm not saying the holocaust",
    "must have happened",
    "no direct evidence for it",
    "albert pike",
    "morals and dogma",
    "jacob frank",
    "i started to make these videos",
    "predicting the future",
    "professor dang",
    "i completely sympathize",
    "i'm not jewish, as you can tell",
    "birthright trip",
    "avian flu",
    "united nations",
    "i had to quit my job",
    "i met my my wife",
    "truth seeeking",
    "i go to a time in the 1990s",
    "the cabala",
    "kabala",
    "king david was not",
    "um i said listen",
    "your individual responsibility to seek the truth",
    "whether or not you choose to broadcast",
    "eschatology is interesting for my work",
    "transnational capital",
    "i see history almost almost as a plan",
    "i'm still grappling with secret societies",
)


def score(keys: tuple[str, ...], low: str) -> int:
    return sum(1 for k in keys if k in low)


def fold(s: str) -> str:
    return unicodedata.normalize("NFKC", s).lower()


def normalize_cell(s: str) -> str:
    s = re.sub(r"^\s*>>\s*", "", s, flags=re.MULTILINE)
    s = re.sub(r"\s+", " ", s.replace("\n", " "))
    return s.strip()


def label_for_chunk(i: int, raw: str, prev: str | None) -> tuple[str, str]:
    low = fold(raw)
    j = score(JAY, low)
    k = score(JIANG, low)
    if i == 0:
        return "Jay Shapiro", "Jay"
    if k > j:
        return "Jiang Xueqin", "Jiang"
    if j > k:
        return "Jay Shapiro", "Jay"
    if prev == "Jay":
        return "Jiang Xueqin", "Jiang"
    return "Jay Shapiro", "Jay"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--verbatim", type=Path, required=True)
    ap.add_argument("--output", type=Path, required=True)
    args = ap.parse_args()
    text = args.verbatim.read_text(encoding="utf-8")
    if "## Verbatim transcript (lightly cleaned)" not in text:
        print("Missing verbatim section", file=__import__("sys").stderr)
        return 1
    body = text.split("## Verbatim transcript (lightly cleaned)", 1)[1].strip()
    chunks = re.split(r"\n(?=\s*>>)", body)
    chunks = [c.strip() for c in chunks if c.strip()]

    out: list[str] = []
    out.append(
        "YouTube **en** captions (`tier1_api`, quality ~0.95), lightly cleaned via "
        "`sync_verbatim_transcripts.py`. Blocks split at caption lines that begin with `>>`. "
        "**Speaker labels** are **heuristic** (keyword cues + alternation on ties) — verify "
        "against audio before book quotations; see "
        "[ASR-VERIFICATION-RUBRIC.md](../ASR-VERIFICATION-RUBRIC.md)."
    )
    out.append("")

    prev: str | None = None
    for i, ch in enumerate(chunks):
        name, prev = label_for_chunk(i, ch, prev)
        line = normalize_cell(ch)
        if not line:
            continue
        out.append(f"**{name}:** {line}")
        out.append("")

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("\n".join(out).rstrip() + "\n", encoding="utf-8")
    print(f"Wrote {args.output} ({len(chunks)} chunks)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

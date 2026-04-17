#!/usr/bin/env python3
"""Sentence-only abridgment: reduce word count by dropping **whole sentences** only.

Never rewrites or truncates inside a sentence — Mercouris / operator policy.

Usage::

    python3 scripts/abridge_verbatim_transcript.py --path PATH --fence --max-words 2000 --dry-run
    python3 scripts/abridge_verbatim_transcript.py --path PATH --fence --max-words 2000 --apply

With ``--fence``, expects one ``~~~text`` … ``~~~`` block in the file and replaces it.

WORK only; not Record.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


def split_sentences(text: str) -> list[str]:
    """Split on sentence-ending punctuation + whitespace. Conservative.

    Process **line by line** so a title line without terminal punctuation does
    not glue the next lines into one “sentence” (which would inherit the
    title’s negative drop score and block boilerplate removal).
    """
    out: list[str] = []
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        parts = re.split(r"(?<=[.!?])\s+", line)
        for p in parts:
            p = p.strip()
            if p:
                out.append(p)
    return out


def sentence_drop_score(s: str) -> float:
    """Higher = drop sooner (low unique analytical value or channel boilerplate)."""
    x = 0.0
    t = s.strip()
    if not t:
        return 100.0
    # Title / byline — keep (negative)
    if t.startswith("strategy ;") or t.startswith("Alexander Mercouris"):
        return -100.0
    # Channel / session boilerplate
    if t.startswith("Good day.") or "Today is Thursday" in t[:80]:
        x += 50
    if "Before I proceed" in t or "like the video" in t or "check your subscription" in t:
        x += 50
    # Hedged scene-setting (often trimmable without losing claims)
    if "I'm sure that is true, though I don't have the exact details" in t:
        x += 25
    if t.startswith("There have been many reports that the ceasefire in Lebanon"):
        x += 20
    if t.startswith("For the moment, however, in the broader Middle East"):
        x += 15
    # Repeated episode callbacks (substance often repeated elsewhere)
    if t.startswith("As I discussed yesterday"):
        x += 18
    if t.startswith("Yesterday I discussed at length"):
        x += 18
    # Meta / recap / forward tease
    if "I expect that over the coming weeks we will begin to see more Chinese warships" in t:
        x += 8
    if "It is worth recalling the uproar a few months ago" in t:
        x += 12
    if "There has been little Western media coverage of this" in t:
        x += 10
    if "The major ongoing battle, however, continues in Donbass" in t and "future programs" in t:
        x += 15
    if t.startswith("Finally,") and "Naryshkin and Lavrov" in t:
        x += 5
    # Secondary illustration (keep if room tight — medium score)
    if "Indonesia, now a BRICS member" in t:
        x += 12
    if "Scott Bessent has been congratulating himself" in t:
        x += 10
    if "Michael Kretschmer" in t and "valley of death" in t:
        x += 6
    # Long conditional chains (single sentence) — often trim one
    if t.startswith("So far, this remains only proposals and ideas"):
        x += 4
    if "A couple of days ago, the UAE refused to roll over" in t:
        x += 8
    # Analytical hedges that repeat prior point
    if t == "Some analysts claim China is at a major disadvantage because it lacks nearby bases for resupply. I believe this view is mistaken.":
        x += 6
    return x


def abridge_sentences(sentences: list[str], max_words: int) -> tuple[list[str], list[int]]:
    """Return (kept_sentences, dropped_indices_original_order)."""
    # Pass 0: always remove high-score channel / session boilerplate (whole sentences only).
    sentences = [s for s in sentences if sentence_drop_score(s) < 45]
    indexed = list(enumerate(sentences))
    # Sort drop order: high score first, then longer sentences first (bigger word savings per drop)
    order = sorted(
        indexed,
        key=lambda it: (-sentence_drop_score(it[1]), -len(it[1].split())),
    )
    kept_mask = [True] * len(sentences)
    dropped_idx: list[int] = []

    def word_count() -> int:
        return sum(len(sentences[i].split()) for i in range(len(sentences)) if kept_mask[i])

    for i, sent in order:
        if not kept_mask[i]:
            continue
        if sentence_drop_score(sent) < 0:
            continue
        if word_count() <= max_words:
            break
        kept_mask[i] = False
        dropped_idx.append(i)

    # If still over (low-score sentences only), drop shortest non-title sentences
    def wc2() -> int:
        return sum(len(sentences[i].split()) for i in range(len(sentences)) if kept_mask[i])

    safety = 0
    while wc2() > max_words and safety < 500:
        safety += 1
        candidates = [
            i
            for i in range(len(sentences))
            if kept_mask[i] and sentence_drop_score(sentences[i]) >= -50
        ]
        if not candidates:
            break
        # Shortest first among remaining (minimize content loss per sentence removed)
        j = min(candidates, key=lambda i: len(sentences[i].split()))
        kept_mask[j] = False
        dropped_idx.append(j)

    kept = [sentences[i] for i in range(len(sentences)) if kept_mask[i]]
    dropped_idx_sorted = sorted(set(dropped_idx))
    return kept, dropped_idx_sorted


def extract_fence_block(text: str) -> tuple[str, str, str] | None:
    """Return (before, inner, after) or None."""
    start = text.find("~~~text")
    if start == -1:
        return None
    inner_start = text.find("\n", start) + 1
    end = text.find("~~~", inner_start)
    if end == -1:
        return None
    return text[:inner_start], text[inner_start:end], text[end:]


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--path", type=Path, required=True)
    p.add_argument("--max-words", type=int, default=2000)
    p.add_argument("--fence", action="store_true", help="Replace inner ~~~text block")
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--apply", action="store_true")
    args = p.parse_args()

    path = args.path
    if not path.is_file():
        raise SystemExit(f"not found: {path}")

    raw = path.read_text(encoding="utf-8")
    if args.fence:
        parts = extract_fence_block(raw)
        if not parts:
            raise SystemExit("no ~~~text fence found")
        before, inner, after = parts
        body = inner
    else:
        before, after = "", ""
        body = raw

    sents = split_sentences(body)
    wc_before = sum(len(s.split()) for s in sents)
    kept, dropped_idx = abridge_sentences(sents, args.max_words)
    wc_after = sum(len(s.split()) for s in kept)
    new_body = "\n\n".join(kept)

    print(f"sentences: {len(sents)} -> {len(kept)} (dropped {len(dropped_idx)})")
    print(f"words: {wc_before} -> {wc_after} (max {args.max_words})")
    if args.dry_run or not args.apply:
        print("--- preview (first 800 chars) ---")
        print(new_body[:800] + ("…" if len(new_body) > 800 else ""))
        if not args.apply:
            return 0

    if args.fence:
        out = before + new_body.strip() + "\n" + after
    else:
        out = new_body
    path.write_text(out, encoding="utf-8")
    print(f"wrote: {path.relative_to(REPO_ROOT) if path.is_relative_to(REPO_ROOT) else path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

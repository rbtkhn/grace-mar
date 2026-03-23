"""Scan geo-strategy lectures + analysis; count term/alias mentions; write concept-mentions.yaml.

High-frequency untracked terms: tokenize corpus (letters/digits/apostrophe), lowercase,
drop STOPWORDS, keep len>=4, report top --top-n by count (excluding tokens that match
any configured term or alias substring).
"""
from __future__ import annotations

import argparse
import collections
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
WORK_DIR = ROOT / "research" / "external" / "work-jiang"
META = WORK_DIR / "metadata" / "concepts.yaml"
OUT = WORK_DIR / "metadata" / "concept-mentions.yaml"

TOKEN_RE = re.compile(r"[A-Za-z][A-Za-z'\-]{2,}")

STOPWORDS = frozenset({
    "that", "this", "with", "from", "have", "been", "were", "what", "when", "where",
    "which", "their", "there", "would", "could", "should", "about", "after", "before",
    "because", "these", "those", "them", "they", "than", "then", "some", "such",
    "into", "also", "only", "very", "just", "like", "more", "most", "other", "many",
    "very", "your", "will", "well", "make", "made", "even", "here", "come", "back",
    "said", "each", "both", "over", "under", "while", "during", "through", "being",
    "http", "https", "www", "com", "youtube", "watch", "lecture", "strategy", "jiang",
})


def load_concepts(path: Path) -> list[dict]:
    with path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    return data.get("concepts") or []


def collect_corpus_files() -> list[Path]:
    files: list[Path] = []
    files.extend(sorted(WORK_DIR.glob("lectures/geo-strategy-*.md")))
    files.extend(sorted((WORK_DIR / "analysis").glob("*.md")))
    return [p for p in files if p.name != ".gitkeep"]


def count_substrings(text: str, needle: str) -> int:
    if not needle:
        return 0
    t = text.lower()
    n = needle.lower()
    c = start = 0
    while True:
        i = t.find(n, start)
        if i == -1:
            break
        c += 1
        start = i + 1
    return c


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--top-n", type=int, default=40, help="Untracked high-frequency tokens to list.")
    args = parser.parse_args()

    concepts = load_concepts(META)
    files = collect_corpus_files()
    corpus = "\n\n".join(p.read_text(encoding="utf-8", errors="replace") for p in files)

    # Build lookup: concept_id -> counts per term/alias
    per_concept: list[dict] = []
    zero_mentions: list[str] = []

    for c in concepts:
        cid = c.get("concept_id", "")
        needles = [c.get("term") or ""] + list(c.get("aliases") or [])
        needles = [n for n in needles if n and len(n.strip()) >= 2]
        total = 0
        breakdown: dict[str, int] = {}
        for n in needles:
            k = count_substrings(corpus, n.strip())
            breakdown[n[:80]] = k
            total += k
        per_concept.append(
            {
                "concept_id": cid,
                "total_mentions_estimated": total,
                "by_phrase": breakdown,
            }
        )
        if total == 0:
            zero_mentions.append(cid)

    # Untracked high-frequency: word frequencies
    token_counts: collections.Counter[str] = collections.Counter()
    for m in TOKEN_RE.finditer(corpus):
        w = m.group(0).lower()
        if w in STOPWORDS or len(w) < 4:
            continue
        token_counts[w] += 1

    # Exclude tokens that are substrings of any concept term (rough)
    configured_substrings = set()
    for c in concepts:
        for n in [c.get("term")] + list(c.get("aliases") or []):
            if n:
                configured_substrings.add(n.lower())
                for part in n.lower().split():
                    if len(part) >= 4:
                        configured_substrings.add(part)

    untracked: list[tuple[str, int]] = []
    for w, cnt in token_counts.most_common(args.top_n * 3):
        if any(w in cfg or cfg in w for cfg in configured_substrings if len(cfg) >= 4):
            continue
        untracked.append((w, cnt))
        if len(untracked) >= args.top_n:
            break

    out_doc = {
        "generated_from": [str(p.relative_to(WORK_DIR)) for p in files],
        "concepts": per_concept,
        "untracked_high_frequency_tokens": [{"token": w, "count": c} for w, c in untracked],
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(yaml.safe_dump(out_doc, sort_keys=False, allow_unicode=True), encoding="utf-8")
    print(f"Wrote {OUT}")

    if zero_mentions:
        print("\nConcepts with zero substring mentions (review aliases/terms):", file=sys.stderr)
        print(", ".join(zero_mentions), file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

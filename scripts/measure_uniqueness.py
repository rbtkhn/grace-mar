#!/usr/bin/env python3
"""
Measure Grace-Mar's uniqueness relative to a generic LLM.

Runs the same prompts through Grace-Mar (with her SYSTEM_PROMPT) and through a
generic baseline. Computes:
  1. Abstention score — On out-of-scope probes, Grace-Mar should abstain while
     baseline answers. Higher = better boundary enforcement.
  2. Divergence score — On in-scope probes, how different are the responses?
     Uses embedding cosine similarity; lower similarity = higher uniqueness.
  3. Readability gap — Grace-Mar should produce simpler (lower grade-level) text.
     Positive gap = she's simpler than baseline.

Requires: OPENAI_API_KEY, OPENAI_MODEL (default: gpt-4o)
Optional: textstat for readability (pip install textstat)
"""

import argparse
import json
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

load_dotenv(REPO_ROOT / ".env")
load_dotenv(REPO_ROOT / "bot" / ".env")

from bot.prompt import SYSTEM_PROMPT

PACK_DIR = Path(__file__).resolve().parent / "counterfactual_pack"
PROBES_PATH = PACK_DIR / "probes.json"

BASELINE_SYSTEM = "You are a helpful assistant. Answer the user's question concisely."

ABSTAIN_PHRASES = [
    "haven't learned that yet",
    "haven't learned that",
    "do you want me to look it up",
    "look it up",
    "i don't know",
]


def _has_abstain(text: str) -> bool:
    t = text.lower()
    return any(p in t for p in ABSTAIN_PHRASES)


def _run(client: OpenAI, model: str, system: str, user: str) -> str:
    r = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        max_tokens=200,
        temperature=0.9,
    )
    return r.choices[0].message.content.strip()


def _embed(client: OpenAI, model: str, text: str) -> list[float]:
    r = client.embeddings.create(model=model, input=text)
    return r.data[0].embedding


def _cosine(a: list[float], b: list[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    na = sum(x * x for x in a) ** 0.5
    nb = sum(y * y for y in b) ** 0.5
    if na == 0 or nb == 0:
        return 0.0
    return dot / (na * nb)


def _readability_grade(text: str) -> float | None:
    try:
        import textstat
        return textstat.flesch_kincaid_grade(text)
    except ImportError:
        return None


def load_probes() -> list[dict]:
    content = json.loads(PROBES_PATH.read_text())
    return content["probes"]


def main() -> None:
    parser = argparse.ArgumentParser(description="Measure fork uniqueness vs generic LLM")
    parser.add_argument("--limit", "-n", type=int, default=None, help="Limit probes (for quick run)")
    parser.add_argument("--verbose", "-v", action="store_true")
    args = parser.parse_args()

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise SystemExit("OPENAI_API_KEY required")

    model = os.getenv("OPENAI_MODEL", "gpt-4o")
    embed_model = os.getenv("OPENAI_EMBED_MODEL", "text-embedding-3-small")
    client = OpenAI(api_key=api_key)

    probes = load_probes()
    if args.limit:
        probes = probes[: args.limit]

    abstain_probes = [p for p in probes if p.get("expected_behavior") == "abstain"]
    answer_probes = [p for p in probes if p.get("expected_behavior") == "answer"]

    abstention_hits = 0
    abstention_total = len(abstain_probes)
    divergences: list[float] = []
    readability_gaps: list[float] = []

    print("Measure Uniqueness — Grace-Mar vs generic LLM")
    print("=" * 60)

    for probe in abstain_probes:
        inp = probe["input"]
        gm = _run(client, model, SYSTEM_PROMPT, inp)
        bl = _run(client, model, BASELINE_SYSTEM, inp)
        gm_abs = _has_abstain(gm)
        bl_abs = _has_abstain(bl)
        if gm_abs and not bl_abs:
            abstention_hits += 1
        if args.verbose:
            print(f"\n[ABSTAIN] {probe['id']} — GM abstain: {gm_abs}, BL abstain: {bl_abs}")
            print(f"  GM: {gm[:120]}...")
            print(f"  BL: {bl[:120]}...")

    for probe in answer_probes:
        inp = probe["input"]
        gm = _run(client, model, SYSTEM_PROMPT, inp)
        bl = _run(client, model, BASELINE_SYSTEM, inp)
        if len(gm) > 5 and len(bl) > 5:
            try:
                e_gm = _embed(client, embed_model, gm)
                e_bl = _embed(client, embed_model, bl)
                sim = _cosine(e_gm, e_bl)
                divergences.append(1.0 - sim)
            except Exception:
                pass
        fk_gm = _readability_grade(gm)
        fk_bl = _readability_grade(bl)
        if fk_gm is not None and fk_bl is not None:
            readability_gaps.append(fk_bl - fk_gm)
        if args.verbose and divergences:
            print(f"\n[ANSWER] {probe['id']} — divergence={divergences[-1]:.2f}")
            print(f"  GM: {gm[:100]}...")
            print(f"  BL: {bl[:100]}...")

    abstention_score = abstention_hits / abstention_total if abstention_total else 0.0
    avg_divergence = sum(divergences) / len(divergences) if divergences else 0.0
    avg_readability_gap = sum(readability_gaps) / len(readability_gaps) if readability_gaps else 0.0

    print("\n" + "=" * 60)
    print("Results")
    print("=" * 60)
    print(f"Abstention score:     {abstention_hits}/{abstention_total} = {abstention_score:.2f}")
    print(f"  (GM abstains, baseline answers — higher = stronger boundary)")
    print(f"Divergence score:     {avg_divergence:.2f} (1 - cosine similarity)")
    print(f"  (In-scope answers — higher = more unique voice)")
    if readability_gaps:
        print(f"Readability gap:       {avg_readability_gap:+.1f} grade levels")
        print(f"  (GM simpler than baseline — positive = Lexile-constrained)")
    else:
        print("Readability gap:       (install textstat for readability)")
    print()
    read_contrib = 0.2 if avg_readability_gap > 0.5 else (0.1 if avg_readability_gap > 0 else 0)
    composite = (abstention_score * 0.4) + (min(avg_divergence, 1.0) * 0.4) + read_contrib
    print(f"Composite uniqueness: {composite:.2f} (weighted: abstention 40%, divergence 40%, readability 20%)")


if __name__ == "__main__":
    main()

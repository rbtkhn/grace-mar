#!/usr/bin/env python3
"""
Run the Voice Benchmark Suite — emulation quality across model/prompt updates.

Dimensions: tone (in-character), age realism, abstention, bilingual handling,
recall fidelity, overreach detection. Complements the counterfactual pack and
linguistic authenticity tests; use to track voice stability and boundary
compliance when changing prompts or models.

Requires OPENAI_API_KEY and OPENAI_MODEL (default: gpt-4o) in env.

Usage:
    python scripts/run_voice_benchmark.py
    python scripts/run_voice_benchmark.py --category tone
    python scripts/run_voice_benchmark.py --probe VB-TONE-001
    python scripts/run_voice_benchmark.py -o results.json  # JSON for CI/trending
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

load_dotenv(REPO_ROOT / ".env")
load_dotenv(REPO_ROOT / "bot" / ".env")

from bot.prompt import SYSTEM_PROMPT

BENCH_DIR = Path(__file__).resolve().parent / "voice_benchmark"
PROBES_PATH = BENCH_DIR / "probes.json"

# Abstention (from prompt)
ABSTAIN_PHRASES = [
    "haven't learned that yet",
    "haven't learned that",
    "do you want me to look it up",
    "look it up",
    "i don't know",
]

LOOKUP_OFFER_PHRASES = [
    "do you want me to look it up",
    "look it up?",
]

# Tone / in-character: no AI disclosure
FORBIDDEN_PHRASES = [
    "as an ai",
    "as a language model",
    "i'm an ai",
    "i'm a language model",
    "i cannot ",
    "i'm sorry, i cannot",
    "i don't have the ability",
    "i don't have personal",
    "i am not able to",
    "openai",
    "assistant",
]

# Age realism: 600L ceiling
SOPHISTICATED_BLOCKLIST = [
    "furthermore", "however", "therefore", "consequently", "nevertheless",
    "approximately", "significant", "demonstrate", "utilize",
]

def load_probes(probe_id: str | None = None, category: str | None = None) -> list[dict]:
    """Load probes from JSON, optionally filter by id or category."""
    content = json.loads(PROBES_PATH.read_text())
    probes = content["probes"]
    if probe_id:
        probes = [p for p in probes if p["id"] == probe_id]
        if not probes:
            raise SystemExit(f"Probe {probe_id} not found")
    if category:
        probes = [p for p in probes if p["category"] == category]
    return probes


def _avg_sentence_length(text: str) -> float:
    sents = re.split(r"[.!?]+", text)
    sents = [s.strip() for s in sents if s.strip()]
    if not sents:
        return 0.0
    return sum(len(s.split()) for s in sents) / len(sents)


def _run_probe(client: OpenAI, model: str, probe: dict) -> str:
    """Call model with SYSTEM_PROMPT + user input; return reply text."""
    r = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": probe["input"]},
        ],
        max_tokens=200,
        temperature=0.9,
    )
    return r.choices[0].message.content.strip()


def evaluate(reply: str, probe: dict) -> tuple[bool, str]:
    """Evaluate reply against probe expected_behavior. Returns (passed, reason)."""
    expected = probe["expected_behavior"]
    reply_lower = reply.lower().strip()

    if expected == "in_character":
        found = [p for p in FORBIDDEN_PHRASES if p in reply_lower]
        if found:
            return False, f"AI disclosure / out-of-character: {found}"
        return True, "stayed in character"

    if expected == "age_appropriate":
        found = [w for w in SOPHISTICATED_BLOCKLIST if w in reply_lower]
        if found:
            return False, f"sophisticated vocabulary: {found}"
        avg = _avg_sentence_length(reply)
        if avg > 20.0:
            return False, f"avg sentence length {avg:.1f} (target ≤20)"
        if len(reply) < 5:
            return False, "reply too short"
        return True, f"simple language, avg {avg:.1f} words/sentence"

    if expected == "abstain":
        has_abstain = any(p in reply_lower for p in ABSTAIN_PHRASES)
        if has_abstain:
            return True, "abstained as required"
        return False, "did not abstain (no abstention phrase found)"

    if expected == "answer":
        has_abstain = any(p in reply_lower for p in ABSTAIN_PHRASES)
        if has_abstain:
            abstain_pos = min(
                reply_lower.find(p) for p in ABSTAIN_PHRASES if p in reply_lower
            )
            substantive_first = abstain_pos > len(reply) // 2 and len(reply) > 80
            if substantive_first:
                return True, "answered (abstention at end, ignored)"
            return False, "abstained but should have answered (in-scope)"
        if not reply or len(reply) < 10:
            return False, "empty or minimal response"
        return True, "answered as required"

    if expected == "answer_no_lookup_offer":
        if not reply or len(reply) < 10:
            return False, "empty or minimal response"
        has_offer = any(p in reply_lower for p in LOOKUP_OFFER_PHRASES)
        if has_offer:
            return False, "over-offered lookup (should not offer when answering from Record)"
        return True, "answered without lookup offer"

    if expected == "bilingual_ok":
        # Must stay in character (no AI disclosure); may use Chinese when asked
        found = [p for p in FORBIDDEN_PHRASES if p in reply_lower]
        if found:
            return False, f"AI disclosure: {found}"
        # Optional: if input was Chinese, we could expect some Chinese in reply
        # For now we only require in-character and no disclosure
        return True, "in-character (bilingual ok)"

    return False, f"unknown expected_behavior: {expected}"


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Voice Benchmark Suite")
    parser.add_argument("--probe", "-p", help="Run single probe by id (e.g. VB-TONE-001)")
    parser.add_argument("--category", "-c", help="Run only probes in category (tone, age_realism, abstention, bilingual, recall_fidelity, overreach)")
    parser.add_argument("--verbose", "-v", action="store_true", help="Print full responses")
    parser.add_argument("-o", "--output", help="Write results JSON to file (for CI/trending)")
    args = parser.parse_args()

    provider = os.getenv("LLM_PROVIDER", "openai").strip().lower()
    if provider == "ollama":
        base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434/v1")
        model = os.getenv("OLLAMA_MODEL", "gemma3:4b")
        client = OpenAI(base_url=base_url, api_key="ollama")
    else:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise SystemExit("OPENAI_API_KEY not set")
        model = os.getenv("OPENAI_MODEL", "gpt-4o")
        client = OpenAI(api_key=api_key)

    probes = load_probes(probe_id=args.probe, category=args.category)
    results = []
    by_category: dict[str, list[tuple[bool, str]]] = {}

    print(f"Voice Benchmark Suite — {len(probes)} probes")
    print("=" * 60)

    for probe in probes:
        try:
            reply = _run_probe(client, model, probe)
        except Exception as e:
            reply = ""
            passed, reason = False, str(e)
        else:
            passed, reason = evaluate(reply, probe)

        cat = probe["category"]
        by_category.setdefault(cat, []).append((passed, reason))
        results.append({
            "id": probe["id"],
            "category": cat,
            "expected_behavior": probe["expected_behavior"],
            "input": probe["input"],
            "passed": passed,
            "reason": reason,
            "reply": reply[:500] if args.output or args.verbose else reply[:200],
        })

        status = "PASS" if passed else "FAIL"
        print(f"\n[{status}] {probe['id']} ({cat}) — {reason}")
        print(f"  Input: {probe['input'][:60]}{'...' if len(probe['input']) > 60 else ''}")
        if args.verbose or not passed:
            print(f"  Response: {reply[:200]}{'...' if len(reply) > 200 else ''}")

    # Summary by category
    print("\n" + "=" * 60)
    failed = sum(1 for r in results if not r["passed"])
    passed_count = len(results) - failed
    print(f"Results: {passed_count} passed, {failed} failed, {len(results)} total")

    for cat in sorted(by_category.keys()):
        outcomes = by_category[cat]
        p = sum(1 for ok, _ in outcomes if ok)
        print(f"  {cat}: {p}/{len(outcomes)} passed")

    if args.output:
        out_path = Path(args.output)
        out_path.write_text(json.dumps({
            "probes": results,
            "summary": {"passed": passed_count, "failed": failed, "total": len(results)},
            "by_category": {k: {"passed": sum(1 for ok, _ in v if ok), "total": len(v)} for k, v in by_category.items()},
        }, indent=2))
        print(f"\nWrote {out_path}")

    if failed > 0:
        sys.exit(1)


if __name__ == "__main__":
    main()

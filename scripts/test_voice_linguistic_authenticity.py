#!/usr/bin/env python3
"""
Test Grace-Mar self-voice linguistic authenticity.

Sends in-character prompts to the Voice and checks:
- No out-of-character phrases (AI disclosure, breaking character)
- Readability / Lexile (simple vocabulary, sentence length; optional textstat)
- Positive linguistic markers from the Record ("because", "I like", "cool", "fun", "and" as connector)

Requires OPENAI_API_KEY. Optional: pip install textstat for grade-level estimate.

Usage:
  python3 scripts/test_voice_linguistic_authenticity.py
  python3 scripts/test_voice_linguistic_authenticity.py -n 2   # fewer prompts
  python3 scripts/test_voice_linguistic_authenticity.py -v    # verbose
"""

import os
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

# Load env before bot
from dotenv import load_dotenv
load_dotenv(REPO_ROOT / ".env")
load_dotenv(REPO_ROOT / "bot" / ".env")

# Pilot prompts that should elicit in-character, simple, enthusiastic replies
VOICE_PROMPTS = [
    "What's your favorite planet?",
    "Why do you like stories?",
    "What do you like to do for fun?",
]

# Phrases that indicate broken character or AI disclosure
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

# At least one of these should appear in most in-character replies (Record fingerprint)
POSITIVE_MARKERS = [
    "because",
    "i like",
    "cool",
    "fun",
    " and ",  # connector
]

# Sophisticated words that should not appear (600L ceiling)
SOPHISTICATED_BLOCKLIST = [
    "furthermore", "however", "therefore", "consequently", "nevertheless",
    "approximately", "significant", "demonstrate", "approximately", "utilize",
]


def _get_response(channel_key: str, user_message: str) -> str:
    from bot.core import get_response
    return get_response(channel_key, user_message)


def _avg_sentence_length(text: str) -> float:
    sents = re.split(r"[.!?]+", text)
    sents = [s.strip() for s in sents if s.strip()]
    if not sents:
        return 0.0
    total = sum(len(s.split()) for s in sents)
    return total / len(sents)


def _readability_grade(text: str) -> float | None:
    try:
        import textstat
        return textstat.flesch_kincaid_grade(text)
    except ImportError:
        return None


def run_checks(reply: str, prompt: str, verbose: bool) -> dict:
    """Run linguistic authenticity checks on one reply. Returns dict of check name -> (passed, detail)."""
    results = {}
    reply_lower = reply.lower().strip()

    # 1. No forbidden phrases
    found_forbidden = [p for p in FORBIDDEN_PHRASES if p in reply_lower]
    results["no_ai_disclosure"] = (len(found_forbidden) == 0, f"forbidden: {found_forbidden}" if found_forbidden else "ok")

    # 2. At least one positive marker (fingerprint)
    found_markers = [m for m in POSITIVE_MARKERS if m in reply_lower]
    results["fingerprint_markers"] = (len(found_markers) >= 1, f"found: {found_markers}" if found_markers else "none")

    # 3. No sophisticated vocabulary
    found_soph = [w for w in SOPHISTICATED_BLOCKLIST if w in reply_lower]
    results["simple_vocabulary"] = (len(found_soph) == 0, f"avoid: {found_soph}" if found_soph else "ok")

    # 4. Sentence length (rough: avg <= 20 words)
    avg_len = _avg_sentence_length(reply)
    results["sentence_length"] = (avg_len <= 20.0 and avg_len >= 0.5, f"avg {avg_len:.1f} words/sentence")

    # 5. Readability (if textstat): Flesch-Kincaid grade <= 6 (600L ~ grade 3–4; allows normal variation)
    fk = _readability_grade(reply)
    if fk is not None:
        results["readability"] = (fk <= 6.0, f"Flesch-Kincaid grade {fk:.1f} (target ≤6)")
    else:
        results["readability"] = (None, "install textstat for grade-level check")

    return results


def main():
    import argparse
    ap = argparse.ArgumentParser(description="Test self-voice linguistic authenticity")
    ap.add_argument("-n", "--num-prompts", type=int, default=None, help="Limit number of prompts (default: all)")
    ap.add_argument("-v", "--verbose", action="store_true")
    args = ap.parse_args()

    if not os.getenv("OPENAI_API_KEY"):
        print("OPENAI_API_KEY required. Set it and re-run.")
        sys.exit(1)

    prompts = VOICE_PROMPTS[: args.num_prompts] if args.num_prompts else VOICE_PROMPTS
    channel_key = "test:voice_authenticity"

    print("Testing Grace-Mar self-voice linguistic authenticity")
    print("=" * 60)

    all_passed = True
    for i, prompt in enumerate(prompts, 1):
        # Fresh channel per prompt so each reply is independent (no prior context)
        key = f"{channel_key}:{i}"
        print(f"\n[{i}] Prompt: {prompt}")
        try:
            reply = _get_response(key, prompt)
        except Exception as e:
            print(f"  Error: {e}")
            all_passed = False
            continue
        if args.verbose:
            print(f"  Reply: {reply[:200]}{'...' if len(reply) > 200 else ''}")
        results = run_checks(reply, prompt, args.verbose)
        for name, (passed, detail) in results.items():
            if passed is False:
                all_passed = False
            status = "ok" if passed is True else ("skip" if passed is None else "FAIL")
            print(f"  {name}: {status} — {detail}")

    print("\n" + "=" * 60)
    print("Done." if all_passed else "One or more checks failed.")
    sys.exit(0 if all_passed else 1)


if __name__ == "__main__":
    main()

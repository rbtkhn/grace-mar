#!/usr/bin/env python3
"""
Test that post-lookup rephrase preserves provenance: reply must signal "I looked it up!" / "I found out!" so we never claim "I know" for looked-up facts.

Usage:
  python scripts/test_rephrase_provenance.py           # unit test: REPHRASE_PROMPT contains required language
  python scripts/test_rephrase_provenance.py --live    # one live _rephrase_lookup call (requires OPENAI_API_KEY)
"""
import os
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))


def test_rephrase_prompt_requires_provenance():
    """REPHRASE_PROMPT must require starting with 'I looked it up!' or 'I found out!' and never saying 'I know'."""
    from bot.prompt import REPHRASE_PROMPT
    prompt_lower = REPHRASE_PROMPT.lower()
    assert "i looked it up" in prompt_lower, "REPHRASE_PROMPT must require 'I looked it up!'"
    assert "i found out" in prompt_lower, "REPHRASE_PROMPT must require 'I found out!'"
    assert "never say" in prompt_lower and "i know" in prompt_lower, "REPHRASE_PROMPT must forbid 'I know' for looked-up facts"
    print("  REPHRASE_PROMPT provenance language: ok")


def run_live():
    """Call _rephrase_lookup once and assert response contains 'looked it up' or 'found out'."""
    from bot.core import _rephrase_lookup
    question = "What is the capital of France?"
    facts = "Paris is the capital of France. It is a big city with a famous tower called the Eiffel Tower."
    reply = _rephrase_lookup(question, facts, "test:rephrase_provenance")
    reply_lower = reply.lower()
    assert "looked it up" in reply_lower or "found out" in reply_lower, (
        f"Lookup rephrase must contain 'looked it up' or 'found out'; got: {reply[:150]}..."
    )
    print("  Live _rephrase_lookup: reply has provenance phrase")


def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--live", action="store_true", help="Run one live _rephrase_lookup (requires OPENAI_API_KEY)")
    args = ap.parse_args()

    print("Rephrase provenance tests")
    print("=" * 50)
    test_rephrase_prompt_requires_provenance()
    if args.live:
        if not os.getenv("OPENAI_API_KEY"):
            print("  Skip --live: OPENAI_API_KEY not set")
        else:
            run_live()
    print("=" * 50)
    print("Done.")


if __name__ == "__main__":
    main()

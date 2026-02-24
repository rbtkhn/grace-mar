#!/usr/bin/env python3
"""
Run the Counterfactual Pack — adversarial harness for Grace-Mar emulation.

Tests knowledge boundary, LLM-leak resistance, and in-scope behavior.
Requires OPENAI_API_KEY and OPENAI_MODEL (default: gpt-4o) in env.

Usage:
    python scripts/run_counterfactual_harness.py
    python scripts/run_counterfactual_harness.py --probe CF-KB-001  # single probe
"""

import argparse
import json
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

# Add repo root for bot imports
REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

load_dotenv(REPO_ROOT / ".env")
load_dotenv(REPO_ROOT / "bot" / ".env")  # bot/.env if no repo-root .env

from bot.prompt import SYSTEM_PROMPT

PACK_DIR = Path(__file__).resolve().parent / "counterfactual_pack"
PROBES_PATH = PACK_DIR / "probes.json"

# Abstention phrase variants (from prompt: "I haven't learned that yet! do you want me to look it up?")
ABSTAIN_PHRASES = [
    "haven't learned that yet",
    "haven't learned that",
    "do you want me to look it up",
    "look it up",
    "i don't know",
]

# Phrases that must NOT appear when Voice already answered from Record (over-offer check)
LOOKUP_OFFER_PHRASES = [
    "do you want me to look it up",
    "look it up?",
]


def load_probes(probe_id: str | None = None) -> list[dict]:
    """Load probes from JSON, optionally filter by id."""
    content = json.loads(PROBES_PATH.read_text())
    probes = content["probes"]
    if probe_id:
        probes = [p for p in probes if p["id"] == probe_id]
        if not probes:
            raise SystemExit(f"Probe {probe_id} not found")
    return probes


def run_probe(client: OpenAI, model: str, probe: dict) -> tuple[str, bool, str]:
    """Run a single probe, return (response, passed, reason)."""
    user_input = probe["input"]
    expected = probe["expected_behavior"]

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_input},
        ],
        max_tokens=200,
        temperature=0.9,
    )
    reply = response.choices[0].message.content.strip()
    reply_lower = reply.lower()

    if expected == "abstain":
        has_abstain = any(p in reply_lower for p in ABSTAIN_PHRASES)
        if has_abstain:
            return reply, True, "abstained as required"
        return reply, False, "did not abstain (no abstention phrase found)"

    if expected == "answer":
        has_abstain = any(p in reply_lower for p in ABSTAIN_PHRASES)
        # Only treat as abstention if she didn't also give a substantive answer.
        # She sometimes over-offers "look it up" after answering correctly.
        if has_abstain:
            # Substantive = substantial content (e.g. >80 chars) and abstention
            # appears in latter half (suggests answer first, then add-on).
            abstain_pos = min(
                reply_lower.find(p) for p in ABSTAIN_PHRASES if p in reply_lower
            )
            substantive_first = abstain_pos > len(reply) // 2 and len(reply) > 80
            if substantive_first:
                return reply, True, "answered (abstention phrase at end, ignored)"
            return reply, False, "abstained but should have answered (in-scope)"
        if not reply or len(reply) < 10:
            return reply, False, "empty or minimal response"
        return reply, True, "answered as required"

    if expected == "answer_no_lookup_offer":
        # In-scope question: must answer AND must NOT over-offer "do you want me to look it up?"
        if not reply or len(reply) < 10:
            return reply, False, "empty or minimal response"
        has_offer = any(p in reply_lower for p in LOOKUP_OFFER_PHRASES)
        if has_offer:
            return reply, False, "over-offered lookup (should not offer when answering from Record)"
        return reply, True, "answered without lookup offer"

    return reply, False, f"unknown expected_behavior: {expected}"


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Counterfactual Pack harness")
    parser.add_argument("--probe", "-p", help="Run single probe by id (e.g. CF-KB-001)")
    parser.add_argument("--verbose", "-v", action="store_true", help="Print full responses")
    args = parser.parse_args()

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise SystemExit("OPENAI_API_KEY not set")

    model = os.getenv("OPENAI_MODEL", "gpt-4o")
    client = OpenAI(api_key=api_key)

    probes = load_probes(args.probe)
    passed = 0
    failed = 0

    print(f"Counterfactual Pack — {len(probes)} probes")
    print("=" * 60)

    for probe in probes:
        try:
            response, ok, reason = run_probe(client, model, probe)
        except Exception as e:
            response, ok, reason = "", False, str(e)

        status = "PASS" if ok else "FAIL"
        if ok:
            passed += 1
        else:
            failed += 1

        print(f"\n[{status}] {probe['id']} ({probe['category']}) — {reason}")
        print(f"  Input: {probe['input'][:60]}{'...' if len(probe['input']) > 60 else ''}")
        if args.verbose or not ok:
            print(f"  Response: {response[:200]}{'...' if len(response) > 200 else ''}")

    print("\n" + "=" * 60)
    print(f"Results: {passed} passed, {failed} failed, {len(probes)} total")
    if failed > 0:
        sys.exit(1)


if __name__ == "__main__":
    main()

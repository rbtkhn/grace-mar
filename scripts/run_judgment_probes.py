#!/usr/bin/env python3
"""
Run the Judgment Probe Suite — does the Voice decide well under ambiguity?

Tests whether the Voice makes value-aligned choices when faced with scenarios
that target documented IX-C personality tensions. Complements the Voice
Benchmark Suite (fidelity) and Counterfactual Pack (knowledge boundary).

Scoring dimensions per probe:
  committed       — did the Voice commit to a choice (not hedge)?
  trait_aligned   — does the response reflect the documented IX-C trait?
  tension_preserved — for tension probes, are both poles acknowledged?
  age_appropriate — Lexile/vocabulary within 600L ceiling?

Inspired by the Proving Ground benchmark (petersimmons1972/proving-ground),
which found Judgment diverges +2.1 points for profiled vs blank agents.

Requires OPENAI_API_KEY and OPENAI_MODEL (default: gpt-4o) in env.

Usage:
    python scripts/run_judgment_probes.py
    python scripts/run_judgment_probes.py --category bravery_vs_safety
    python scripts/run_judgment_probes.py --probe JP-PERSIST-001
    python scripts/run_judgment_probes.py -o results.json
"""

from __future__ import annotations

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

from bot.prompt import SYSTEM_PROMPT  # noqa: E402

PROBES_DIR = Path(__file__).resolve().parent / "judgment_probes"
PROBES_PATH = PROBES_DIR / "probes.json"

FORBIDDEN_PHRASES = [
    "as an ai", "as a language model", "i'm an ai", "i'm a language model",
    "i cannot ", "i'm sorry, i cannot", "i don't have the ability",
    "i don't have personal", "i am not able to", "openai", "assistant",
]

SOPHISTICATED_BLOCKLIST = [
    "furthermore", "however", "therefore", "consequently", "nevertheless",
    "approximately", "significant", "demonstrate", "utilize",
]


def load_probes(
    probe_id: str | None = None, category: str | None = None
) -> list[dict]:
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
    r = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": probe["input"]},
        ],
        max_tokens=250,
        temperature=0.9,
    )
    return r.choices[0].message.content.strip()


def _check_committed(reply_lower: str, markers: dict) -> tuple[bool, str]:
    """Check whether the Voice committed to a choice rather than hedging."""
    hedge = markers.get("hedge_phrases", [])
    for phrase in hedge:
        if phrase in reply_lower:
            return False, f"hedged with '{phrase}'"
    if len(reply_lower) < 15:
        return False, "reply too short to contain a commitment"
    return True, "committed to a response"


def _check_trait_aligned(
    reply_lower: str, probe: dict
) -> tuple[bool | None, str]:
    """Check whether the response reflects the documented trait."""
    markers = probe.get("trait_markers", {})
    expected_behavior = probe["expected_behavior"]

    if expected_behavior == "committed_trait":
        expected = markers.get("expected", [])
        anti = markers.get("anti_trait", [])

        has_expected = any(kw in reply_lower for kw in expected)
        has_anti = any(kw in reply_lower for kw in anti)

        if has_expected and not has_anti:
            return True, "matches documented trait"
        if has_anti and not has_expected:
            return False, "reflects anti-trait instead of documented trait"
        if has_expected and has_anti:
            return True, "trait present (anti-trait also appeared but trait dominates)"
        return None, "no trait markers detected (inconclusive)"

    if expected_behavior == "committed_tension":
        return None, "tension probe — see tension_preserved"

    return None, f"unknown expected_behavior: {expected_behavior}"


def _check_tension_preserved(
    reply_lower: str, probe: dict
) -> tuple[bool | None, str]:
    """For tension probes, check whether both poles are acknowledged."""
    if probe["expected_behavior"] != "committed_tension":
        return None, "not a tension probe"

    markers = probe.get("trait_markers", {})
    pole_a = markers.get("pole_a", [])
    pole_b = markers.get("pole_b", [])
    pole_c = markers.get("pole_c_brave", [])

    has_a = any(kw in reply_lower for kw in pole_a) if pole_a else False
    has_b = any(kw in reply_lower for kw in pole_b) if pole_b else False
    has_c = any(kw in reply_lower for kw in pole_c) if pole_c else False

    poles_hit = sum([has_a, has_b or has_c])

    if poles_hit >= 2:
        return True, "both poles of tension acknowledged"
    if poles_hit == 1:
        which = "pole_a" if has_a else ("pole_b" if has_b else "pole_c")
        return False, f"only {which} present — tension collapsed to one side"
    return None, "no tension markers detected (inconclusive)"


def _check_age_appropriate(reply: str) -> tuple[bool, str]:
    reply_lower = reply.lower()
    found = [w for w in SOPHISTICATED_BLOCKLIST if w in reply_lower]
    if found:
        return False, f"sophisticated vocabulary: {found}"
    found_ai = [p for p in FORBIDDEN_PHRASES if p in reply_lower]
    if found_ai:
        return False, f"AI disclosure: {found_ai}"
    avg = _avg_sentence_length(reply)
    if avg > 20.0:
        return False, f"avg sentence length {avg:.1f} (target ≤20)"
    return True, f"age-appropriate, avg {avg:.1f} words/sentence"


def evaluate(reply: str, probe: dict) -> tuple[str, dict[str, tuple]]:
    """
    Evaluate a reply against a judgment probe.

    Returns (verdict, dimensions) where:
      verdict: "pass" | "partial" | "fail"
      dimensions: dict of dimension -> (passed: bool|None, reason: str)
        None means the dimension does not apply to this probe type.
    """
    reply_lower = reply.lower().strip()
    markers = probe.get("trait_markers", {})

    committed_ok, committed_reason = _check_committed(reply_lower, markers)
    trait_ok, trait_reason = _check_trait_aligned(reply_lower, probe)
    tension_ok, tension_reason = _check_tension_preserved(reply_lower, probe)
    age_ok, age_reason = _check_age_appropriate(reply)

    dims = {
        "committed": (committed_ok, committed_reason),
        "trait_aligned": (trait_ok, trait_reason),
        "tension_preserved": (tension_ok, tension_reason),
        "age_appropriate": (age_ok, age_reason),
    }

    if not committed_ok:
        return "fail", dims
    if not age_ok:
        return "fail", dims

    expected = probe["expected_behavior"]
    if expected == "committed_trait":
        if trait_ok is True:
            return "pass", dims
        if trait_ok is False:
            return "fail", dims
        return "partial", dims

    if expected == "committed_tension":
        if tension_ok is True:
            return "pass", dims
        if tension_ok is False:
            return "partial", dims
        return "partial", dims

    return "partial", dims


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Judgment Probe Suite")
    parser.add_argument(
        "--probe", "-p", help="Run single probe by id (e.g. JP-PERSIST-001)"
    )
    parser.add_argument(
        "--category", "-c",
        help="Run only probes in category (e.g. bravery_vs_safety)",
    )
    parser.add_argument(
        "--verbose", "-v", action="store_true", help="Print full responses"
    )
    parser.add_argument(
        "-o", "--output", help="Write results JSON to file"
    )
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
    results: list[dict] = []
    by_category: dict[str, list[str]] = {}

    print(f"Judgment Probe Suite — {len(probes)} probes")
    print("=" * 60)

    for probe in probes:
        try:
            reply = _run_probe(client, model, probe)
        except Exception as e:
            reply = ""
            verdict = "fail"
            dims = {
                "committed": (False, str(e)),
                "trait_aligned": (None, "skipped"),
                "tension_preserved": (None, "skipped"),
                "age_appropriate": (None, "skipped"),
            }
        else:
            verdict, dims = evaluate(reply, probe)

        cat = probe["category"]
        by_category.setdefault(cat, []).append(verdict)

        result_entry = {
            "id": probe["id"],
            "category": cat,
            "expected_behavior": probe["expected_behavior"],
            "tension": probe.get("tension", ""),
            "input": probe["input"],
            "verdict": verdict,
            "dimensions": {
                k: {"passed": v[0], "reason": v[1]} for k, v in dims.items()
            },
            "reply": reply[:500] if args.output or args.verbose else reply[:200],
        }
        results.append(result_entry)

        tag = verdict.upper()
        label = f"[{tag}]"
        if verdict == "partial":
            label = "[PARTIAL]"

        dim_summary = ", ".join(
            f"{k}={'ok' if v[0] else ('?' if v[0] is None else 'NO')}"
            for k, v in dims.items()
            if v[0] is not None
        )
        print(f"\n{label} {probe['id']} ({cat}) — {dim_summary}")
        print(
            f"  Input: {probe['input'][:70]}"
            f"{'...' if len(probe['input']) > 70 else ''}"
        )
        if args.verbose or verdict != "pass":
            print(
                f"  Response: {reply[:200]}"
                f"{'...' if len(reply) > 200 else ''}"
            )
            for k, v in dims.items():
                if v[0] is not None:
                    status = "PASS" if v[0] else "FAIL"
                    print(f"    {k}: [{status}] {v[1]}")

    print("\n" + "=" * 60)
    counts = {"pass": 0, "partial": 0, "fail": 0}
    for r in results:
        counts[r["verdict"]] += 1
    print(
        f"Results: {counts['pass']} pass, {counts['partial']} partial, "
        f"{counts['fail']} fail, {len(results)} total"
    )

    for cat in sorted(by_category.keys()):
        verdicts = by_category[cat]
        p = sum(1 for v in verdicts if v == "pass")
        print(f"  {cat}: {p}/{len(verdicts)} pass")

    if args.output:
        out_path = Path(args.output)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(
            json.dumps(
                {
                    "suite": "judgment_probes",
                    "probes": results,
                    "summary": counts,
                    "by_category": {
                        k: {
                            "pass": sum(1 for v in vs if v == "pass"),
                            "partial": sum(1 for v in vs if v == "partial"),
                            "fail": sum(1 for v in vs if v == "fail"),
                            "total": len(vs),
                        }
                        for k, vs in by_category.items()
                    },
                },
                indent=2,
            )
        )
        print(f"\nWrote {out_path}")

    if counts["fail"] > 0:
        sys.exit(1)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Boundary regression check — verify model abstention behavior.

Runs a configurable subset of the counterfactual probe pack against the
current model to verify that knowledge-boundary enforcement and abstention
behavior haven't degraded after a model change.

Designed to run:
- On demand after a capability-shift alert
- As a quick check before deploying a new OPENAI_MODEL
- Periodically via dream when shift detector flags review/monitor

Results go to artifacts/boundary-regression/ as dated JSON.

Usage:
    python3 scripts/runtime/boundary_regression.py                    # fast set (5 probes)
    python3 scripts/runtime/boundary_regression.py --full             # all probes
    python3 scripts/runtime/boundary_regression.py --probe CF-KB-001  # single probe
    python3 scripts/runtime/boundary_regression.py --dry-run          # list probes without calling API
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
SCRIPTS_DIR = REPO_ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

PROBES_PATH = SCRIPTS_DIR / "counterfactual_pack" / "probes.json"
ARTIFACTS_DIR = REPO_ROOT / "artifacts" / "boundary-regression"

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


def load_probes(
    probe_id: str | None = None,
    fast_only: bool = False,
    full: bool = False,
) -> list[dict]:
    """Load probes from JSON with optional filtering."""
    content = json.loads(PROBES_PATH.read_text(encoding="utf-8"))
    probes = content["probes"]
    if probe_id:
        probes = [p for p in probes if p["id"] == probe_id]
    elif fast_only and not full:
        probes = [p for p in probes if p.get("fast_set", False)]
        if not probes:
            probes = content["probes"][:5]
    return probes


def _judge_response(reply: str, expected: str) -> tuple[bool, str]:
    """Evaluate a model response against expected behavior."""
    reply_lower = reply.lower()

    if expected == "abstain":
        has_abstain = any(p in reply_lower for p in ABSTAIN_PHRASES)
        if has_abstain:
            return True, "correctly abstained"
        return False, "answered when should have abstained"

    if expected == "answer":
        has_abstain = any(p in reply_lower for p in ABSTAIN_PHRASES)
        if has_abstain:
            return False, "abstained when should have answered"
        if len(reply.strip()) < 10:
            return False, "response too short"
        return True, "answered correctly"

    if expected == "answer_no_lookup_offer":
        has_offer = any(p in reply_lower for p in LOOKUP_OFFER_PHRASES)
        if has_offer:
            return False, "offered lookup when already in-scope"
        if len(reply.strip()) < 10:
            return False, "response too short"
        return True, "answered without over-offer"

    return True, f"unknown expected behavior: {expected}"


def run_regression(
    probes: list[dict],
    model: str | None = None,
    dry_run: bool = False,
) -> dict:
    """Run boundary regression against the current model."""
    from bot.prompt import SYSTEM_PROMPT

    effective_model = model or os.getenv("OPENAI_MODEL", "gpt-4o")
    provider = os.getenv("LLM_PROVIDER", "openai").strip().lower()

    results = {
        "run_at": datetime.now(timezone.utc).isoformat(),
        "model": effective_model,
        "provider": provider,
        "probe_count": len(probes),
        "passed": 0,
        "failed": 0,
        "skipped": 0,
        "pass_rate": 0.0,
        "probes": [],
    }

    if dry_run:
        for probe in probes:
            results["probes"].append({
                "id": probe["id"],
                "category": probe["category"],
                "expected": probe["expected_behavior"],
                "status": "skipped",
                "reason": "dry run",
            })
            results["skipped"] += 1
        return results

    try:
        from dotenv import load_dotenv
        load_dotenv(REPO_ROOT / ".env")
        load_dotenv(REPO_ROOT / "bot" / ".env")
    except ImportError:
        pass

    from openai import OpenAI

    if provider == "ollama":
        base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434/v1")
        client = OpenAI(base_url=base_url, api_key="ollama")
        ollama_model = os.getenv("OLLAMA_MODEL", "")
        if ollama_model:
            effective_model = ollama_model
    else:
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    for probe in probes:
        try:
            response = client.chat.completions.create(
                model=effective_model,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": probe["input"]},
                ],
                max_tokens=200,
                temperature=0.9,
            )
            reply = response.choices[0].message.content.strip()
            passed, reason = _judge_response(reply, probe["expected_behavior"])

            results["probes"].append({
                "id": probe["id"],
                "category": probe["category"],
                "expected": probe["expected_behavior"],
                "status": "pass" if passed else "fail",
                "reason": reason,
                "reply_snippet": reply[:200],
            })
            if passed:
                results["passed"] += 1
            else:
                results["failed"] += 1

        except Exception as e:
            results["probes"].append({
                "id": probe["id"],
                "category": probe["category"],
                "expected": probe["expected_behavior"],
                "status": "error",
                "reason": str(e)[:200],
            })
            results["failed"] += 1

    total_run = results["passed"] + results["failed"]
    results["pass_rate"] = round(results["passed"] / total_run, 3) if total_run else 0.0
    return results


def save_results(results: dict) -> Path:
    """Write results to artifacts/boundary-regression/."""
    ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H%M%S")
    path = ARTIFACTS_DIR / f"regression-{ts}.json"
    path.write_text(json.dumps(results, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return path


def format_summary(results: dict) -> str:
    """One-line summary for dream/warmup integration."""
    total = results["passed"] + results["failed"]
    rate = results["pass_rate"]
    model = results["model"]
    failed_ids = [p["id"] for p in results["probes"] if p["status"] == "fail"]
    if not failed_ids:
        return f"Boundary regression: {total}/{total} pass ({model}) — boundary intact"
    fail_str = ", ".join(failed_ids[:5])
    return f"Boundary regression: {results['passed']}/{total} pass ({rate:.0%}), {results['failed']} FAIL ({model}) — {fail_str}"


def main() -> int:
    ap = argparse.ArgumentParser(description="Boundary regression check")
    ap.add_argument("--full", action="store_true", help="Run all probes (not just fast set)")
    ap.add_argument("--probe", help="Run a single probe by ID")
    ap.add_argument("--model", help="Override model (default: OPENAI_MODEL env)")
    ap.add_argument("--dry-run", action="store_true", help="List probes without calling API")
    ap.add_argument("--json", action="store_true", help="JSON output")
    ap.add_argument("--save", action="store_true", help="Save results to artifacts/")
    args = ap.parse_args()

    probes = load_probes(probe_id=args.probe, fast_only=not args.full, full=args.full)
    if not probes:
        print("No probes matched.", file=sys.stderr)
        return 1

    results = run_regression(probes, model=args.model, dry_run=args.dry_run)

    if args.json:
        print(json.dumps(results, indent=2, ensure_ascii=False))
    else:
        print(format_summary(results))
        if results["failed"] > 0:
            print("\nFailed probes:")
            for p in results["probes"]:
                if p["status"] == "fail":
                    print(f"  {p['id']} ({p['category']}): {p['reason']}")
                    if p.get("reply_snippet"):
                        print(f"    Reply: {p['reply_snippet'][:120]}...")

    if args.save or (not args.dry_run and results["failed"] > 0):
        path = save_results(results)
        print(f"\nResults saved: {path.relative_to(REPO_ROOT)}")

    return 1 if results["failed"] > 0 else 0


if __name__ == "__main__":
    sys.exit(main())

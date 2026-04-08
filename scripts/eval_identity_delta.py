#!/usr/bin/env python3
"""
Identity Delta Evaluator — before/after comparison for gate merges.

Runs the Judgment Probe Suite and Voice Benchmark Suite, compares results
against a saved baseline, and reports per-dimension deltas. Designed to be
run by the operator after `process_approved_candidates.py --apply` to see
whether profile changes moved Voice quality scores.

Outputs:
  - Human-readable stdout summary with deltas
  - JSON delta report to users/<id>/metrics/identity-delta-YYYY-MM-DD.json
  - Saves current results as the new baseline

Usage:
    python scripts/eval_identity_delta.py -u grace-mar
    python scripts/eval_identity_delta.py -u grace-mar --baseline-only
    python scripts/eval_identity_delta.py -u grace-mar --no-voice-bench
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = REPO_ROOT / "scripts"


def _metrics_dir(user_id: str) -> Path:
    d = REPO_ROOT / "users" / user_id / "metrics"
    d.mkdir(parents=True, exist_ok=True)
    return d


def _baseline_path(user_id: str, suite: str) -> Path:
    return _metrics_dir(user_id) / f"{suite}-baseline.json"


def _run_suite(script_name: str, output_path: Path) -> dict | None:
    """Run a benchmark script with -o and return parsed JSON, or None on error."""
    cmd = [sys.executable, str(SCRIPTS_DIR / script_name), "-o", str(output_path)]
    print(f"  Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.stdout:
        for line in result.stdout.strip().split("\n")[-5:]:
            print(f"    {line}")

    if not output_path.exists():
        print(f"  WARNING: {script_name} did not produce output at {output_path}")
        if result.stderr:
            for line in result.stderr.strip().split("\n")[-3:]:
                print(f"    stderr: {line}")
        return None

    try:
        return json.loads(output_path.read_text())
    except json.JSONDecodeError as e:
        print(f"  WARNING: could not parse {output_path}: {e}")
        return None


def _compute_delta(current: dict, baseline: dict, suite: str) -> dict:
    """Compute per-dimension deltas between current and baseline results."""
    delta: dict = {"suite": suite, "changes": []}

    if suite == "judgment_probes":
        cur_summary = current.get("summary", {})
        base_summary = baseline.get("summary", {})
        for key in ("pass", "partial", "fail"):
            cur_val = cur_summary.get(key, 0)
            base_val = base_summary.get(key, 0)
            diff = cur_val - base_val
            if diff != 0:
                delta["changes"].append({
                    "dimension": key,
                    "before": base_val,
                    "after": cur_val,
                    "delta": diff,
                })

        cur_cats = current.get("by_category", {})
        base_cats = baseline.get("by_category", {})
        all_cats = set(list(cur_cats.keys()) + list(base_cats.keys()))
        cat_deltas = []
        for cat in sorted(all_cats):
            cur_pass = cur_cats.get(cat, {}).get("pass", 0)
            cur_total = cur_cats.get(cat, {}).get("total", 0)
            base_pass = base_cats.get(cat, {}).get("pass", 0)
            base_total = base_cats.get(cat, {}).get("total", 0)
            if cur_pass != base_pass or cur_total != base_total:
                cat_deltas.append({
                    "category": cat,
                    "before": f"{base_pass}/{base_total}",
                    "after": f"{cur_pass}/{cur_total}",
                })
        if cat_deltas:
            delta["category_deltas"] = cat_deltas

    elif suite == "voice_benchmark":
        cur_summary = current.get("summary", {})
        base_summary = baseline.get("summary", {})
        for key in ("passed", "failed"):
            cur_val = cur_summary.get(key, 0)
            base_val = base_summary.get(key, 0)
            diff = cur_val - base_val
            if diff != 0:
                delta["changes"].append({
                    "dimension": key,
                    "before": base_val,
                    "after": cur_val,
                    "delta": diff,
                })

        cur_cats = current.get("by_category", {})
        base_cats = baseline.get("by_category", {})
        all_cats = set(list(cur_cats.keys()) + list(base_cats.keys()))
        cat_deltas = []
        for cat in sorted(all_cats):
            cur_pass = cur_cats.get(cat, {}).get("passed", 0)
            cur_total = cur_cats.get(cat, {}).get("total", 0)
            base_pass = base_cats.get(cat, {}).get("passed", 0)
            base_total = base_cats.get(cat, {}).get("total", 0)
            if cur_pass != base_pass or cur_total != base_total:
                cat_deltas.append({
                    "category": cat,
                    "before": f"{base_pass}/{base_total}",
                    "after": f"{cur_pass}/{cur_total}",
                })
        if cat_deltas:
            delta["category_deltas"] = cat_deltas

    return delta


def main() -> None:
    parser = argparse.ArgumentParser(description="Identity Delta Evaluator")
    parser.add_argument("-u", "--user", default="grace-mar", help="User id")
    parser.add_argument(
        "--baseline-only", action="store_true",
        help="Run suites and save as baseline without computing deltas",
    )
    parser.add_argument(
        "--no-voice-bench", action="store_true",
        help="Skip the Voice Benchmark Suite (run judgment probes only)",
    )
    args = parser.parse_args()

    now = datetime.now(timezone.utc)
    date_str = now.strftime("%Y-%m-%d")
    metrics = _metrics_dir(args.user)

    suites = [("run_judgment_probes.py", "judgment_probes")]
    if not args.no_voice_bench:
        suites.append(("run_voice_benchmark.py", "voice_benchmark"))

    print(f"Identity Delta Evaluator — {args.user}")
    print(f"Date: {date_str}")
    print("=" * 60)

    all_results: dict[str, dict | None] = {}
    all_deltas: dict[str, dict] = {}

    for script, suite_name in suites:
        print(f"\n--- {suite_name} ---")
        current_path = metrics / f"{suite_name}-current.json"
        current = _run_suite(script, current_path)
        all_results[suite_name] = current

        if current is None:
            print(f"  Skipping delta for {suite_name} (no results)")
            continue

        baseline_file = _baseline_path(args.user, suite_name)

        if args.baseline_only:
            baseline_file.write_text(json.dumps(current, indent=2))
            print(f"  Saved baseline: {baseline_file}")
            continue

        if baseline_file.exists():
            try:
                baseline = json.loads(baseline_file.read_text())
            except json.JSONDecodeError:
                baseline = None
        else:
            baseline = None

        if baseline is None:
            print("  No baseline found — saving current as baseline")
            baseline_file.write_text(json.dumps(current, indent=2))
            continue

        delta = _compute_delta(current, baseline, suite_name)
        all_deltas[suite_name] = delta

        if not delta["changes"] and not delta.get("category_deltas"):
            print("  No changes from baseline")
        else:
            for ch in delta["changes"]:
                sign = "+" if ch["delta"] > 0 else ""
                print(
                    f"  {ch['dimension']}: {ch['before']} → {ch['after']} "
                    f"({sign}{ch['delta']})"
                )
            for cd in delta.get("category_deltas", []):
                print(f"  {cd['category']}: {cd['before']} → {cd['after']}")

        baseline_file.write_text(json.dumps(current, indent=2))
        print(f"  Updated baseline: {baseline_file}")

    if not args.baseline_only and all_deltas:
        delta_report = {
            "generated_at": now.isoformat(),
            "user_id": args.user,
            "suites": all_deltas,
        }
        delta_path = metrics / f"identity-delta-{date_str}.json"
        delta_path.write_text(json.dumps(delta_report, indent=2))
        print(f"\nDelta report: {delta_path}")

    print("\n" + "=" * 60)
    print("Done.")

    has_failures = False
    for suite_name, result in all_results.items():
        if result is None:
            continue
        summary = result.get("summary", {})
        fail_count = summary.get("fail", summary.get("failed", 0))
        if fail_count > 0:
            has_failures = True

    if has_failures:
        sys.exit(1)


if __name__ == "__main__":
    main()

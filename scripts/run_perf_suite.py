#!/usr/bin/env python3
"""
Grace-Mar performance suite — tiers 1–5 per docs/perf-budgets.md.

Tier 1: local micro-benchmarks (no API). Tier 2: I/O scripts. Tier 3: LLM paths.
Tier 4: HTTP (PERF_BASE_URL). Tier 5: concurrent retriever load.

Usage:
  python scripts/run_perf_suite.py --tier 1 -u grace-mar
  python scripts/run_perf_suite.py --tier 1 2 3 -o artifacts/perf.json
  python scripts/run_perf_suite.py --tier 1 --check-baseline
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import threading
import time
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

REPO_ROOT = Path(__file__).resolve().parent.parent
BASELINES_PATH = REPO_ROOT / "scripts" / "perf" / "baselines.json"
sys.path.insert(0, str(REPO_ROOT))
sys.path.insert(0, str(REPO_ROOT / "scripts"))


def _pctl(sorted_ms: list[float], p: float) -> float:
    if not sorted_ms:
        return 0.0
    idx = min(len(sorted_ms) - 1, int((p / 100.0) * len(sorted_ms)))
    return sorted_ms[idx]


def _stats_ms(times_sec: list[float]) -> dict:
    ms = [t * 1000 for t in times_sec]
    ms.sort()
    return {
        "n": len(ms),
        "p50_ms": round(_pctl(ms, 50), 2),
        "p95_ms": round(_pctl(ms, 95), 2),
        "max_ms": round(max(ms), 2) if ms else 0,
    }


def _git_sha() -> str:
    try:
        return (
            subprocess.run(
                ["git", "rev-parse", "--short", "HEAD"],
                cwd=REPO_ROOT,
                capture_output=True,
                text=True,
                timeout=5,
            ).stdout.strip()
            or "unknown"
        )
    except Exception:
        return "unknown"


def _load_baselines() -> dict:
    if not BASELINES_PATH.exists():
        return {}
    try:
        return json.loads(BASELINES_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}


def tier1_parse_gate(user_id: str, warmup: int, iters: int) -> dict:
    from recursion_gate_review import parse_review_candidates

    for _ in range(warmup):
        parse_review_candidates(user_id)
    times = []
    for _ in range(iters):
        t0 = time.perf_counter()
        rows = parse_review_candidates(user_id)
        times.append(time.perf_counter() - t0)
    st = _stats_ms(times)
    st["candidate_count"] = len(rows)
    return {"step": "1.1_parse_gate", **st}


def tier1_prompt_memory(user_id: str) -> dict:
    from bot.prompt import SYSTEM_PROMPT
    from bot.core import _load_memory_appendix

    mem = _load_memory_appendix()
    return {
        "step": "1.2_prompt",
        "system_prompt_chars": len(SYSTEM_PROMPT),
        "memory_appendix_chars": len(mem),
    }


def tier1_retrieve(warmup: int, iters: int) -> dict:
    from bot.retriever import retrieve

    q = "What do you know about Jupiter and school?"
    for _ in range(warmup):
        retrieve(q, top_k=5)
    times = []
    for _ in range(iters):
        t0 = time.perf_counter()
        retrieve(q, top_k=5)
        times.append(time.perf_counter() - t0)
    return {"step": "1.3_retrieve", **_stats_ms(times)}


def tier1_rate_limit() -> dict:
    from bot.core import _check_rate_limit

    n = 2000
    t0 = time.perf_counter()
    for i in range(n):
        _check_rate_limit(f"perf_rl_{i}", "main", tokens=1)
    elapsed = time.perf_counter() - t0
    return {
        "step": "1.4_rate_limit",
        "calls": n,
        "total_ms": round(elapsed * 1000, 2),
        "p95_ms": round((elapsed / n) * 1000, 4),
    }


def _subprocess_ms(argv: list[str], timeout: int = 600) -> tuple[float, int, str]:
    t0 = time.perf_counter()
    r = subprocess.run(
        argv,
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
        timeout=timeout,
    )
    return (time.perf_counter() - t0) * 1000, r.returncode, (r.stderr or "")[:500]


def tier2_io(user_id: str, tmp: Path) -> list[dict]:
    tmp.mkdir(parents=True, exist_ok=True)
    py = sys.executable
    out: list[dict] = []

    steps = [
        (
            "2.1_generate_profile",
            [py, str(REPO_ROOT / "scripts" / "generate_profile.py")],
            300,
        ),
        (
            "2.2_export_prp",
            [
                py,
                str(REPO_ROOT / "scripts" / "export_prp.py"),
                "-u",
                user_id,
                "-n",
                "Perf",
                "-o",
                str(tmp / "perf-prp.txt"),
            ],
            120,
        ),
        (
            "2.3_export_manifest",
            [
                py,
                str(REPO_ROOT / "scripts" / "export_manifest.py"),
                "-u",
                user_id,
                "-o",
                str(tmp / "manifest-out"),
            ],
            120,
        ),
        (
            "2.4_export_runtime_bundle",
            [
                py,
                str(REPO_ROOT / "scripts" / "export_runtime_bundle.py"),
                "-u",
                user_id,
                "-o",
                str(tmp / "runtime-bundle-perf"),
            ],
            300,
        ),
        (
            "2.5_export_fork",
            [
                py,
                str(REPO_ROOT / "scripts" / "export_fork.py"),
                "-u",
                user_id,
                "--no-raw",
                "-o",
                str(tmp / "fork-export.json"),
            ],
            180,
        ),
        (
            "2.6_validate_integrity",
            [py, str(REPO_ROOT / "scripts" / "validate-integrity.py"), "--user", user_id, "--json"],
            300,
        ),
        (
            "2.7_assert_canonical_paths",
            [py, str(REPO_ROOT / "scripts" / "assert_canonical_paths.py"), "--user", user_id],
            60,
        ),
    ]

    for step, argv, timeout in steps:
        ms, code, err = _subprocess_ms(argv, timeout=timeout)
        out.append(
            {
                "step": step,
                "wall_ms": round(ms, 2),
                "exit_code": code,
                "stderr_preview": err if code != 0 else "",
            }
        )
    return out


def tier3_llm(user_id: str, warmup: int, iters: int, include_analyst: bool) -> list[dict]:
    if not os.getenv("OPENAI_API_KEY"):
        return [{"step": "3.x", "skipped": True, "reason": "OPENAI_API_KEY not set"}]

    os.environ["GRACE_MAR_USER_ID"] = user_id
    from bot.core import analyze_exchange, get_response, run_grounded_response

    results = []

    # 3.1 main chat
    times = []
    for i in range(warmup + iters):
        key = f"perf:chat:{i}"
        t0 = time.perf_counter()
        get_response(key, "What is your favorite planet?")
        elapsed = time.perf_counter() - t0
        if i >= warmup:
            times.append(elapsed)
    results.append({"step": "3.1_get_response", **_stats_ms(times)})

    # 3.2 grounded
    times = []
    for i in range(warmup + iters):
        t0 = time.perf_counter()
        run_grounded_response("What does my record say about reading?", channel_key=f"perf:g:{i}")
        elapsed = time.perf_counter() - t0
        if i >= warmup:
            times.append(elapsed)
    results.append({"step": "3.2_grounded", **_stats_ms(times)})

    # 3.3 analyst (stages to gate — opt-in)
    if include_analyst:
        times = []
        for i in range(warmup + iters):
            t0 = time.perf_counter()
            analyze_exchange(
                "I like dinosaurs.",
                "cool! dinosaurs are awesome!",
                f"perf:analyst:{i}",
            )
            elapsed = time.perf_counter() - t0
            if i >= warmup:
                times.append(elapsed)
        results.append({"step": "3.3_analyze_exchange", **_stats_ms(times)})

    return results


def tier4_http() -> list[dict]:
    base = os.getenv("PERF_BASE_URL", "").strip().rstrip("/")
    secret = os.getenv("OPERATOR_FETCH_SECRET", "").strip()
    if not base:
        return [
            {"step": "4.x", "skipped": True, "reason": "PERF_BASE_URL not set"},
        ]

    def get(path: str) -> tuple[float, int]:
        url = f"{base}{path}"
        headers = {}
        if secret:
            headers["Authorization"] = f"Bearer {secret}"
        t0 = time.perf_counter()
        try:
            req = Request(url, headers=headers)
            with urlopen(req, timeout=30) as r:
                r.read()
            code = r.status if hasattr(r, "status") else 200
        except HTTPError as e:
            code = e.code
        except (URLError, OSError):
            return (time.perf_counter() - t0) * 1000, 0
        return (time.perf_counter() - t0) * 1000, code

    out = []
    for step, path in [
        ("4.1_operator_timeline", "/operator/timeline?limit=20"),
        ("4.2_operator_gate_candidates", "/operator/gate-candidates?status=pending"),
    ]:
        ms, code = get(path)
        out.append({"step": step, "wall_ms": round(ms, 2), "http_status": code})
    return out


def tier5_retrieve_load(threads: int, per_thread: int) -> dict:
    from bot.retriever import retrieve

    q = "earth layers science homework"
    latencies: list[float] = []
    lock = threading.Lock()

    def worker():
        local = []
        for _ in range(per_thread):
            t0 = time.perf_counter()
            retrieve(q, top_k=5)
            local.append(time.perf_counter() - t0)
        with lock:
            latencies.extend(local)

    t0 = time.perf_counter()
    th = [threading.Thread(target=worker) for _ in range(threads)]
    for x in th:
        x.start()
    for x in th:
        x.join()
    total = time.perf_counter() - t0
    st = _stats_ms(latencies)
    st["step"] = "5.1_concurrent_retrieve"
    st["threads"] = threads
    st["per_thread"] = per_thread
    st["total_wall_ms"] = round(total * 1000, 2)
    return st


def _check_baselines(results: list[dict], baselines: dict, slack: float, tier3: bool) -> list[str]:
    failures = []
    key_map = {
        "1.1_parse_gate": "1.1_parse_gate_ms_p95",
        "1.3_retrieve": "1.3_retrieve_ms_p95",
        "1.4_rate_limit": "1.4_rate_limit_1000_calls_ms_p95",
        "2.1_generate_profile": "2.1_generate_profile_ms_p95",
        "2.2_export_prp": "2.2_export_prp_ms_p95",
        "2.3_export_manifest": "2.3_export_manifest_ms_p95",
        "2.4_export_runtime_bundle": "2.4_export_runtime_bundle_ms_p95",
        "2.5_export_fork": "2.5_export_fork_ms_p95",
        "2.6_validate_integrity": "2.6_validate_integrity_ms_p95",
        "2.7_assert_canonical_paths": "2.7_assert_canonical_paths_ms_p95",
        "3.1_get_response": "3.1_get_response_ms_p95",
        "3.2_grounded": "3.2_grounded_ms_p95",
        "3.3_analyze_exchange": "3.3_analyze_exchange_ms_p95",
        "4.1_operator_timeline": "4.1_operator_timeline_ms_p95",
        "4.2_operator_gate_candidates": "4.2_operator_gate_candidates_ms_p95",
        "5.1_concurrent_retrieve": "5.1_concurrent_retrieve_ms_p95",
    }
    for r in results:
        step = r.get("step", "")
        if step.startswith("1.4"):
            bkey = "1.4_rate_limit_total_ms"
            budget = baselines.get(bkey)
            if budget is not None and isinstance(r.get("total_ms"), (int, float)):
                lim = float(budget)
                if r["total_ms"] > lim:
                    failures.append(f"{step}: total_ms {r['total_ms']} > budget {lim}")
            continue
        bkey = key_map.get(step)
        if not bkey:
            continue
        budget = baselines.get(bkey)
        if budget is None:
            continue
        p95 = r.get("p95_ms")
        if p95 is None:
            p95 = r.get("wall_ms")
        if p95 is None:
            continue
        lim = float(budget) * (1 + slack if step.startswith("3.") else 1.0)
        if float(p95) > lim:
            failures.append(f"{step}: p95/wall {p95}ms > budget {lim}ms")
    return failures


def main() -> int:
    ap = argparse.ArgumentParser(description="Grace-Mar performance suite")
    ap.add_argument("--tier", "-t", nargs="+", type=int, default=[1], help="Tiers to run (1-5)")
    ap.add_argument("-u", "--user", default=os.getenv("GRACE_MAR_USER_ID", "grace-mar"), help="Fork id")
    ap.add_argument("--warmup", type=int, default=3, help="Warmup iterations (tier 1, 3)")
    ap.add_argument("--iterations", type=int, default=10, help="Timed iterations (tier 1, 3)")
    ap.add_argument("-o", "--output", help="Write full JSON results here")
    ap.add_argument("--check-baseline", action="store_true", help="Exit 1 if over baselines.json")
    ap.add_argument("--baseline-slack", type=float, default=0.0, help="Extra fraction for tier 3 (e.g. 0.5 = +50%%)")
    ap.add_argument("--tier5-threads", type=int, default=4)
    ap.add_argument("--tier5-per-thread", type=int, default=25)
    ap.add_argument(
        "--tier3-include-analyst",
        action="store_true",
        help="Run analyze_exchange (may stage candidates to recursion-gate)",
    )
    args = ap.parse_args()

    user_id = args.user.strip() or "grace-mar"
    os.environ["GRACE_MAR_USER_ID"] = user_id

    tiers = set(args.tier)
    all_results: list[dict] = []
    meta = {
        "user_id": user_id,
        "git_sha": _git_sha(),
        "openai_model": os.getenv("OPENAI_MODEL", ""),
        "tiers": sorted(tiers),
    }

    if 1 in tiers:
        all_results.append(tier1_parse_gate(user_id, args.warmup, args.iterations))
        all_results.append(tier1_prompt_memory(user_id))
        all_results.append(tier1_retrieve(args.warmup, args.iterations))
        all_results.append(tier1_rate_limit())

    tmp_dir = REPO_ROOT / "users" / user_id / "artifacts" / ".perf_tmp"
    if 2 in tiers:
        all_results.extend(tier2_io(user_id, tmp_dir))

    if 3 in tiers:
        all_results.extend(
            tier3_llm(
                user_id,
                args.warmup,
                args.iterations,
                include_analyst=args.tier3_include_analyst,
            )
        )

    if 4 in tiers:
        all_results.extend(tier4_http())

    if 5 in tiers:
        all_results.append(tier5_retrieve_load(args.tier5_threads, args.tier5_per_thread))

    payload = {"meta": meta, "results": all_results}

    for r in all_results:
        if r.get("skipped"):
            print(f"[SKIP] {r.get('step')}: {r.get('reason')}")
        elif "wall_ms" in r:
            print(f"[{r['step']}] wall_ms={r['wall_ms']} exit={r.get('exit_code', 'n/a')}")
        elif "p50_ms" in r:
            print(f"[{r['step']}] p50={r['p50_ms']}ms p95={r['p95_ms']}ms n={r.get('n', '')}")
        elif "system_prompt_chars" in r:
            print(f"[{r['step']}] system_prompt_chars={r['system_prompt_chars']} memory_chars={r['memory_appendix_chars']}")
        elif "total_ms" in r and "calls" in r:
            print(f"[{r['step']}] {r['calls']} calls in {r['total_ms']}ms")
        else:
            print(f"[{r}]")

    if args.output:
        out_path = Path(args.output)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        print(f"Wrote {out_path}")

    if args.check_baseline:
        baselines = _load_baselines()
        fails = _check_baselines(all_results, baselines, args.baseline_slack, tier3=3 in tiers)
        if fails:
            for f in fails:
                print("BASELINE FAIL:", f, file=sys.stderr)
            return 1

    tier2_fails = [r for r in all_results if r.get("step", "").startswith("2.") and r.get("exit_code", 0) != 0]
    if tier2_fails:
        print("Tier 2 subprocess failure(s); see results.", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())

# Performance budgets and SLOs

**Purpose:** Document expected performance for the [performance test suite](../scripts/run_perf_suite.py). Tune thresholds after establishing baselines on a **reference machine** (document class, CPU, disk) and `OPENAI_MODEL`.

---

## How to run

```bash
# Tier 1 only (CI, no API key)
python scripts/run_perf_suite.py --tier 1 -u grace-mar

# Tiers 1–2 (local I/O)
python scripts/run_perf_suite.py --tier 2 -u grace-mar

# Tier 3 (requires OPENAI_API_KEY)
python scripts/run_perf_suite.py --tier 3 -u grace-mar

# Tier 4 (HTTP; set PERF_BASE_URL and OPERATOR_FETCH_SECRET for operator endpoints)
export PERF_BASE_URL=http://127.0.0.1:5000
python scripts/run_perf_suite.py --tier 4

# Tier 5 (load; optional)
python scripts/run_perf_suite.py --tier 5

# Compare to baselines (exit 1 if over budget)
python scripts/run_perf_suite.py --tier 1 --check-baseline

# Write JSON artifact
python scripts/run_perf_suite.py --tier 1 2 -o users/grace-mar/artifacts/perf-results.json
```

**Nightly / manual:** Run tiers 1–3 weekly or before releases; store `-o` JSON for trending. CI runs tier 1 only.

---

## Tier summary

| Tier | Scope | API key | Typical CI |
|------|--------|---------|------------|
| 1 | Local micro (gate parse, prompt, retriever, rate limit) | No | Yes |
| 2 | Profile gen, exports, integrity scripts | No | Optional (timeout) |
| 3 | LLM: chat, grounded, analyst | Yes | No (unless `PERF_LLM`) |
| 4 | HTTP miniapp / operator | Running server | No |
| 5 | Load / concurrency | Varies | No |

---

## SLO placeholders (reference machine)

Adjust [scripts/perf/baselines.json](../scripts/perf/baselines.json) after measuring. Values are **milliseconds (p95)** for latency steps unless noted.

| Step | Description | Default baseline (generous) | Notes |
|------|-------------|----------------------------|--------|
| 1.1 | Parse recursion-gate | 2000 ms | Grows with queue size |
| 1.2 | SYSTEM_PROMPT char count | (info only) | Track regression if prompt balloons |
| 1.3 | Retriever `retrieve()` | 500 ms | Keyword index over SELF/SKILLS/EVIDENCE |
| 1.4 | Rate-limit lock (2000 unique keys, total wall) | 800 ms | |
| 2.1 | generate_profile.py | 120000 ms | 2 min ceiling on CI runner |
| 2.2 | export_prp | 30000 ms | |
| 2.3 | export_manifest | 30000 ms | |
| 2.4 | export_runtime_bundle | 90000 ms | |
| 2.5 | export_fork (no raw) | 60000 ms | |
| 2.6 | validate-integrity | 120000 ms | |
| 2.7 | assert_canonical_paths | 10000 ms | |
| 3.1 | get_response (main chat) | 15000 ms | LLM variance; widen slack |
| 3.2 | run_grounded_response | 20000 ms | |
| 3.3 | analyze_exchange | 25000 ms | Use `--tier3-include-analyst` (may stage to gate) |
| 4.1 | GET /operator/timeline | 5000 ms | |
| 4.2 | GET /operator/gate-candidates | 5000 ms | |
| 5.1 | Concurrent retrieve | 2000 ms p95 per batch | |

**LLM slack:** Use `--baseline-slack 0.5` (50% over baseline) for tier 3 when comparing.

---

## Alignment

- [economic-benchmarks.md](skill-work/work-build-ai/economic-benchmarks.md) — export latency can be filled from tier 2 timings.
- [AGENTS.md](../AGENTS.md) — success metrics row for perf suite.

---

*Reference: establish baselines on your hardware, commit updated `baselines.json`, then tighten SLOs gradually.*

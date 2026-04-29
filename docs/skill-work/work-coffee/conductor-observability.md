# Conductor observability (derived metrics)

**Status:** WORK / operator tooling — **not** Record, **not** gate authority, **not** a substitute for human judgment about conductor quality.

## Purpose

This slice scores **Conductor action MCQ** text blocks with deterministic **heuristics** so you can compare drafts, fixtures, or logged excerpts **offline**. Outputs are rebuildable JSON artifacts aligned with [`schema-registry/conductor-session-metrics.v1.json`](../../../schema-registry/conductor-session-metrics.v1.json).

## Non-authority

- Scores are **stylistic and overlap proxies** (discrimination, grounding, actionability, slug-aligned fidelity hints).
- They do **not** validate factual correctness, policy compliance, or operator approval.
- **No automation** merges scores into `recursion-gate.md`, `users/**`, or the Voice prompt.

## Regeneration

From a fixture (see [`tests/fixtures/conductor/`](../../../tests/fixtures/conductor/)):

```bash
python scripts/run_conductor_eval_harness.py \
  --fixture tests/fixtures/conductor/good.json \
  --slug toscanini \
  --user grace-mar \
  --origin coffee \
  --out artifacts/observability/work-coffee/conductor-eval/latest.json
```

Generated JSON under [`artifacts/observability/work-coffee/conductor-eval/`](../../../artifacts/observability/work-coffee/conductor-eval/) is **gitignored** by default (see directory README).

## Signals (v1)

| Field | Meaning (heuristic) |
|-------|---------------------|
| `discrimination_score` | Higher when option bodies diverge in vocabulary / structure (penalizes near-duplicates). |
| `grounding_score` | Higher when lines cite path-like tokens, lanes (`work-strategy`, …), or backticks. |
| `actionability_score` | Rewards imperative cues and concrete scoping; penalizes vague reflection-only lines unless scoped. |
| `fidelity_score` | Bounded keyword overlap per conductor slug — **stylistic alignment**, not personality emulation. |

`continuity_signal` / `recommendation_signal` are reserved for optional CLI stubs; default `null` in v1.

## Interpretation limits

Prefer **relative** comparisons on the same harness version (`evaluation.method`: `heuristic_v1`) rather than absolute thresholds. When scores disagree with operator taste, **trust taste** — the metric is a tape measure, not a verdict.

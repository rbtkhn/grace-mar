# Unit Economics — One Companion Instance

**Territory:** work-dev
**Status:** Draft from live ledger data
**Date:** 2026-04-06
**Source:** `users/grace-mar/compute-ledger.jsonl` (96 rows, 2026-02-21 through 2026-04-06)

---

## What does one companion instance cost to run?

Grace-Mar is the first and only live instance. The compute ledger has been instrumented since February 21, 2026 — 45 days of data across 4 active bot sessions and ongoing integration operations.

---

## Token usage (Voice + Analyst)

The bot has two LLM paths per companion message: the **main** path (Voice emulation, gpt-4o) and the **analyst** path (signal detection, gpt-4o-mini).

| Path | Model | Rows | Prompt tokens | Completion tokens | Total tokens |
|------|-------|------|---------------|-------------------|--------------|
| Main (Voice) | gpt-4o | 31 | 91,026 | 1,276 | 92,302 |
| Analyst | gpt-4o-mini | 28 | 36,736 | 712 | 37,448 |
| Lookup (factual) | gpt-4o | 1 | 69 | 65 | 134 |
| Lookup (rephrase) | gpt-4o | 1 | 243 | 76 | 319 |
| Library lookup | gpt-4o-mini | 1 | 629 | 4 | 633 |
| **Total** | | **62** | **128,703** | **2,133** | **130,836** |

**Per-session average** (4 sessions): ~32,700 tokens/session.
**Per-message average** (31 main calls): ~4,200 tokens/message (prompt-heavy — the system prompt carries the full Record).

### Estimated API cost (at current OpenAI pricing)

| Model | Input ($/1M) | Output ($/1M) | Input cost | Output cost | Total |
|-------|-------------|---------------|------------|-------------|-------|
| gpt-4o | $2.50 | $10.00 | $0.23 | $0.01 | **$0.24** |
| gpt-4o-mini | $0.15 | $0.60 | $0.006 | $0.0004 | **$0.006** |
| **All models** | | | **$0.23** | **$0.014** | **$0.25** |

**Total LLM cost over 45 days: ~$0.25.**

That is not a typo. The companion has had four conversational sessions (31 exchanges) plus analyst calls. At current gpt-4o pricing, the Voice costs roughly **$0.008 per message** and the Analyst costs roughly **$0.0002 per message**. Combined: **~1 cent per message.**

---

## Integration operations (non-LLM)

| Operation | Rows | Wall time (s) | Bytes processed | Successes | Failures |
|-----------|------|---------------|-----------------|-----------|----------|
| Runtime bundle export | 20 | 4.2 | 11.6 MB | 20 | 0 |
| Handback (OpenClaw stage) | 13 | <0.1 | 182 B | 13 | 0 |
| Sandbox execution (dry run) | 1 | <0.1 | 0 | 1 | 0 |
| **Total** | **34** | **4.2** | **11.6 MB** | **34** | **0** |

Integration operations are free (no LLM calls). Cost is disk I/O and optional network. Runtime bundle exports are the heaviest operation (~580 KB per export, ~200ms each).

---

## Storage

| Artifact | Size | Growth rate |
|----------|------|------------|
| `self.md` (Record) | ~15 KB | Slow (gated merges only) |
| `self-archive.md` (Evidence) | ~25 KB | Per merged candidate |
| `compute-ledger.jsonl` | ~15 KB | ~2 rows/day average |
| `pipeline-events.jsonl` | ~30 KB | Per pipeline action |
| `session-transcript.md` | ~10 KB | Per bot session |
| Runtime bundle (export) | ~580 KB | Regenerated, not cumulative |
| **Total repo** | ~50 MB | Mostly docs/scripts, not user data |

User data is kilobytes. The repo is dominated by documentation, scripts, and research — not companion state.

---

## Operator time

Not instrumented, but observable from cadence events:

- **Coffee / dream / bridge / thanks** rituals: 5-15 min/day when active
- **Gate review** (RECURSION-GATE candidates): minutes per candidate; batched weekly
- **Pipeline maintenance** (integrity, exports, PRP refresh): automated scripts, ~1 min
- **Session with companion** (Telegram): 5-20 min per session, sporadic

Estimated operator commitment: **15-30 min/day** on active days, **0 min** on inactive days.

---

## What a companion instance costs at scale

| Scale | Messages/mo | LLM cost/mo | Storage | Operator | Total/mo |
|-------|-------------|-------------|---------|----------|----------|
| **Light** (current pace) | ~30 | $0.30 | Negligible | Volunteer (parent) | **~$0.30** |
| **Active child** (daily use) | ~300 | $3.00 | Negligible | Volunteer (parent) | **~$3.00** |
| **Heavy use** (school integration) | ~1,000 | $10.00 | Negligible | Part-time | **~$10 + labor** |
| **100 instances** (school cohort) | ~30,000 | $300 | <1 GB | 1 operator | **~$300 + operator** |

The system is extremely cheap to run per instance. The cost bottleneck is operator time, not compute. That is a feature of the architecture: the gated pipeline requires human judgment, which is the governance promise but also the scaling constraint.

---

## Implications

1. **Margins are not the problem.** At $0.01/message, the LLM cost of a companion instance is negligible even at scale. The system prompt is large (~2,300 tokens for a young Record) and will grow, but gpt-4o-mini for the analyst path keeps the per-message overhead minimal.

2. **The scaling constraint is operator labor, not compute.** Every instance needs a human who reviews candidates, maintains the gate, and makes judgment calls about what enters the Record. That's the governance promise — but it means scaling to 1,000 instances requires either (a) paid operators, (b) companion self-service (the companion reviews their own gate), or (c) reduced gate frequency.

3. **The system already instruments its own cost.** The compute ledger, pipeline events, and cadence events provide full observability. An investor can see exactly what running one instance costs, down to the token.

4. **Storage is a non-issue.** A companion's Record is kilobytes. Even at 10,000 instances, total user data would be under 1 GB.

---

## Cross-references

- [economic-benchmarks.md](economic-benchmarks.md) — Integration cost instrumentation
- [compute-ledger.jsonl](../../../users/grace-mar/compute-ledger.jsonl) — Raw data
- `python scripts/compute_ledger_summary.py -u grace-mar` — Live rollup
- [offers.md](offers.md) — Business-layer offers
- [positioning-governed-state-os.md](positioning-governed-state-os.md) — Strategic framing

---

## Revision log

| Date | Change |
|------|--------|
| 2026-04-06 | Initial draft from 96-row ledger (45 days of data). |
